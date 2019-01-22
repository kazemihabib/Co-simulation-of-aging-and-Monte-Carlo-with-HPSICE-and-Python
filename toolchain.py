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
    file_data_line_by_line = f.read().split('\n')

    file_line_by_line_with_no_monte = []
    monte_data = None
    for line in file_data_line_by_line:
        gaussian = regexParser.parse_guassian_distribution(line)
        monte = regexParser.parse_monte(line)
        include = regexParser.parse_include(line)

        if include:
            line = include[0] + include[1] + "../../" + include[2] 
        if gaussian:
            distribution_map[gaussian[0]] = gaussian[1:]
        elif monte:
            monte_data = monte
            file_line_by_line_with_no_monte.append(monte_data[0])
        else:
            file_line_by_line_with_no_monte.append(line)

    return (file_line_by_line_with_no_monte, distribution_map, monte_data)

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

def generate_process_variation(spice_file, path):
    result = initial_spice_parse(spice_file)
    lines = result[0]
    distribution_map = result[1]
    print(distribution_map)
    if distribution_map == {}:
        return (False, "Distribution not found", None)
    monte = result[2]
    if monte == None:
        return (False, ".tran XXX XXX sweep monte=XXX didn't found", None)
    monte_runs = int(monte[1])
    generated_files = []
    for i in range(monte_runs):
        new_lines = parse_spice(lines, i, distribution_map)
        generated_files.append(utils.write_to_file(spice_file, i, path, new_lines))

    return (True, "", generated_files)
    
def main():
    args = handle_args() 
    if args[0] == False:
        print(args[1])
        return
    arg_options = args[1]
    path = utils.get_path_to_generate_temp_data(arg_options[__SPICE_FILE])
    print(path)
    generated = generate_process_variation(arg_options[__SPICE_FILE], path)
    if generated[0] == False:
        print(generated[1])
    else:
        if generated[2] is None:
            print("Unexpedted error happened")
        else :
            for path in generated[2]:
                utils.run_hspice(path)


if __name__ == "__main__":
    main()
