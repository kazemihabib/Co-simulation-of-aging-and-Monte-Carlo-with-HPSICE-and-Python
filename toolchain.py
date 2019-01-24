import sys
import random
import regexParser
import utils

distribution_map = {}

__SPICE_FILE = "spice_file"
__SCRIPT_FILE = "script_file"

def handle_args():
    args = sys.argv
    print(args)
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
    for line in file_data_line_by_line:
        gaussian = regexParser.parse_guassian_distribution(line)
        tran_sweep = regexParser.parse_monte(line)
        include = regexParser.parse_include(line)

        if include:
            line = include[0] + include[1] + "../../../" + include[2] 
        if gaussian:
            distribution_map[gaussian[0]] = gaussian[1:]
        elif tran_sweep:
            tran_sweep_data = tran_sweep 
            file_line_by_line_with_no_monte.append(tran_sweep_data[0])
        else:
            file_line_by_line_with_no_monte.append(line)

    return (file_line_by_line_with_no_monte, distribution_map, tran_sweep_data, aging_part)

# Calculates the Width and Length from given distribution
def calculate_distribution(line, index, distribution_map):
    # Fix this and calculate the variables based on distribution_map
    new_line = ""
    size = regexParser.parse_tran_size(line[2])
    size[0] = str(int(size[0]) + random.uniform(0, 1))
    line[2] = ''.join(size)

    line[3] = ''

    size = regexParser.parse_tran_size(line[6])
    size[0] = str(int(size[0]) + random.uniform(0, 1))
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

def generate_step1(monte_runs, lines, ):
    pass

def generate_step2():
    pass

def generate_process_variation(initialised_data, step1_path, step2_path, name, aging_part):
    # result = initial_spice_parse(spice_file)
    lines = initialised_data[0]
    distribution_map = initialised_data[1]
    print(distribution_map)
    if distribution_map == {}:
        return (False, "Distribution not found", None)
    tran_sweep_data = initialised_data[2]
    if tran_sweep_data == None:
        return (False, ".tran XXX XXX sweep monte=XXX didn't found", None)
    monte_runs = int(tran_sweep_data[1])
    step1_generated_files = []
    step2_generated_files = []
    for i in range(monte_runs):
        step1_lines = parse_spice(lines, i, distribution_map)
        step2_lines = utils.add_aging_part(step1_lines, aging_part).split('\n') 

        step1_generated_files.append(utils.write_to_file(name, i, step1_path, step1_lines))
        step2_generated_files.append(utils.write_to_file(name, i, step2_path, step2_lines))
    
    return (True, "", step1_generated_files, step2_generated_files)
    
def main():
    args = handle_args() 
    if args[0] == False:
        print(args[1])
        return
    arg_options = args[1]
    step1_path = utils.get_path_to_generate_step_data(arg_options[__SPICE_FILE], 1)
    step2_path = utils.get_path_to_generate_step_data(arg_options[__SPICE_FILE], 2)
    print(step1_path)
    initialised_data = initial_spice_parse(arg_options[__SPICE_FILE])
    generated = generate_process_variation(initialised_data, step1_path, step2_path, arg_options[__SPICE_FILE], initialised_data[3])
    if generated[0] == False:
        print(generated[1])
    else:
        if generated[2] == [] or generated[3] == []:
            print("Unexpedted error happened")
        else :
            for path in generated[2]:
                utils.run_hspice(path)

            for path in generated[3]:
                utils.run_hspice(path)


if __name__ == "__main__":
    main()
