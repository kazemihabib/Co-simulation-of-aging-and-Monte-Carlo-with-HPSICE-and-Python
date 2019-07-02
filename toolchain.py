import sys
import random
import regexParser
import utils
import numpy as np
import os
import math

distribution_map = {}

__SPICE_FILE = "spice_file"
__SCRIPT_FILE = "script_file"
monte_runs = 0

def handle_args():
    args = sys.argv
    message = "The correct way to run this program is: python3 toolchain.py -i yourspicefile.sp -s yourscripts.py "
    if len(args) < 3:
        return (False, message)

    cont = True 
    arg_dict = {}
    for i in range(len(args)):
        if cont == True:
            cont = False
            continue

        if args[i] == '-i':
            arg_dict[__SPICE_FILE] = args[i+1]
            cont == True

    if __SPICE_FILE not in arg_dict: 
        return (False, message)

    return (True, arg_dict)

# Parses hspice file and prepare it
# 1) Fixes the include line to get file (Note: in current version the library should be beside the spice file)
# 2) Removes GAUSSIAN Distribution (TODO: Add more distributions)
# 3) Removes "sweep monte=XX" from .tran 10p 40n sweep monte=10
def initial_spice_parse(file_name):
    distribution_map = {}

    f = open(file_name)
    (before_aging, aging_part, after_aging) = utils.remove_aging_part(f.read())

    data_to_parse = before_aging + '\n' + after_aging

    file_data_line_by_line = data_to_parse.split('\n')

    file_line_by_line_with_no_monte = []
    tran_sweep_data = None
    measure_variables = []
    for line in file_data_line_by_line:
        gaussian = regexParser.parse_guassian_distribution(line)
        tran_sweep = regexParser.parse_monte(line)
        include = regexParser.parse_include(line)
        measure_variable = regexParser.parse_measure(line)

        if include:
            line = include[0] + include[1] + "../../../" + include[2] 
        if gaussian:
            distribution_map[gaussian[0]] = gaussian[1:]
        elif tran_sweep:
            tran_sweep_data = tran_sweep 
            file_line_by_line_with_no_monte.append(tran_sweep_data[0])
        elif measure_variable:
            measure_variables.append(measure_variable[0])
            file_line_by_line_with_no_monte.append(line)
        else:
            file_line_by_line_with_no_monte.append(line)
    f.close()
    return (file_line_by_line_with_no_monte, distribution_map, tran_sweep_data, aging_part, measure_variables)

def calculate_random(variable, distribution_map):
    (distribution, m, z, x) = distribution_map[variable] 
    sigma = float(m) * float(z) / float(x)
    if str(distribution).upper() == "GAUSS":
        rand = np.random.normal(float(m), float(sigma), 1)
        return rand[0]
    return 1 

# Calculates the Width and Length from given distribution
def calculate_distribution(line, index, distribution_map):
    # Fix this and calculate the variables based on distribution_map
    new_line = ""
    size = regexParser.parse_tran_size(line[2])
    size[0] = str(int(size[0]) * calculate_random(line[3], distribution_map))
    line[2] = ''.join(size)

    line[3] = ''

    size = regexParser.parse_tran_size(line[6])
    size[0] = str(int(size[0]) * calculate_random(line[7], distribution_map))
    line[6] = ''.join(size)

    line[7] = ''        
    new_line = ''.join(line)
    return new_line

#Parses the spice 
def parse_spice(file_lines, index, distribution_map):
    new_file_lines = []
    for line in file_lines:
        sizing_monte = regexParser.parse_sizing_monte(line)
        if sizing_monte:
            line = calculate_distribution(sizing_monte, index, distribution_map)

        new_file_lines.append(line)
    return new_file_lines 

def generate_process_variation(initialised_data, step1_path, step2_path, name, aging_part):
    global monte_runs
    lines = initialised_data[0]
    distribution_map = initialised_data[1]
    if distribution_map == {}:
        return (False, "Distribution not found", None)
    tran_sweep_data = initialised_data[2]
    if tran_sweep_data == None:
        return (False, ".tran XXX XXX sweep monte=XXX didn't found", None)
    monte_runs = int(tran_sweep_data[1])
    step1_generated_in_directory = []
    step2_generated_in_directory = []
    for i in range(monte_runs):
        step1_lines = parse_spice(lines, i, distribution_map)
        step2_lines = utils.add_aging_part(step1_lines, aging_part).split('\n') 

        step1_generated_in_directory.append(utils.write_to_file(name, i, step1_path, step1_lines))
        step2_generated_in_directory.append(utils.write_to_file(name, i, step2_path, step2_lines))
    
    return (True, "", step1_generated_in_directory, step2_generated_in_directory)

def run_hspice(directories_of_step1, directories_of_step2, file_name):
    print("Step1 runs:")
    print("**************************************************************************************")
    step_1_aborts = 0
    step_2_aborts = 0
    res = True
    for directory in directories_of_step1:
        file_path = os.path.join(directory, file_name) 
        res = utils.run_hspice(file_path)
        if not res:
            step_1_aborts+=1

    print("**************************************************************************************")

    print("\n\nStep2 runs:")
    print("**************************************************************************************")
    for directory in directories_of_step2:
        file_path = os.path.join(directory, file_name) 
        res = utils.run_hspice(file_path)
        if not res:
            step_2_aborts+=1

    
    print("**************************************************************************************")
    print("Step1 =>\t {aborted} of {all} aborted".format(aborted=step_1_aborts, all=monte_runs))
    print("Step2 =>\t {aborted} of {all} aborted".format(aborted=step_2_aborts, all=monte_runs))



def calculate_mean(data):
    return sum(data) / len(data)

def calculate_sigma(data):
    mean = calculate_mean(data)
    return math.sqrt( sum([(item - mean) **2 for item in data]) / len(data))

def calculate_delays_from_csv(directories, mt_file_name, measure_variables):
    dic = {}
    for directory in directories:
        file_path = os.path.join(directory, mt_file_name )
        row = utils.read_csv(file_path)

        for column in measure_variables:
            try:
                if column in dic:
                    dic[column].append(float(row[column]))
                else:
                    dic[column] = [float(row[column])]
            except:
                pass #Something failed

    # print("Debug:")
    # print("################################################################\n")
    # print(dic)
    # print("################################################################\n")

    for item in measure_variables:
        data = dic[item]
        print("{name} =>\tmean: {mean}\tsigma: {sigma}".format(name=item, mean=calculate_mean(data), sigma=calculate_sigma(data)))

def calculate_delays(directories_of_step1, directories_of_step2, measure_variables, mt_file_name_step_1, mt_file_name_step_2):
    print("\nSTEP1:")
    print("**************************************************************************************")
    calculate_delays_from_csv(directories_of_step1, mt_file_name_step_1, measure_variables)
    print("**************************************************************************************")

    print("\nSTEP2:")
    print("**************************************************************************************")
    calculate_delays_from_csv(directories_of_step2, mt_file_name_step_2, measure_variables)
    print("**************************************************************************************")

def main():
    args = handle_args() 
    if args[0] == False:
        print(args[1])
        return
    arg_options = args[1]
    step1_path = utils.get_path_to_generate_step_data(arg_options[__SPICE_FILE], 1)
    step2_path = utils.get_path_to_generate_step_data(arg_options[__SPICE_FILE], 2)
    initialised_data = initial_spice_parse(arg_options[__SPICE_FILE])
    generated = generate_process_variation(initialised_data, step1_path, step2_path, arg_options[__SPICE_FILE], initialised_data[3])
    measure_variables = [item.lower() for item in initialised_data[4]]

    if generated[0] == False:
        print(generated[1])
    else:
        if generated[2] == [] or generated[3] == []:
            print("Unexpecdted error happened")
        else :
            run_hspice(generated[2], generated[3], arg_options[__SPICE_FILE])
            mt_file = arg_options[__SPICE_FILE].split('.')
            mt_file_name_step_1 = mt_file[0] + '.mt0.csv'
            mt_file_name_step_2 = mt_file[0] + '.mt0@ra.csv'

            calculate_delays(generated[2], generated[3], measure_variables, mt_file_name_step_1, mt_file_name_step_2)


if __name__ == "__main__":
    main()
