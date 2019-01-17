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
    message = "The correct way to this program is: python3 toolchain.py -i yourspicefile.sp -s yourscripts.py "
    if len(args) < 5:
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
        elif args[i] == "-s":
            arg_dict[__SCRIPT_FILE] = args[i+1].split('.')[0] #remove .py
            cont = True

    if __SPICE_FILE not in arg_dict or __SCRIPT_FILE not in arg_dict:
        return (False, message)

    return (True, arg_dict)

def initial_spice_parse(file_name):
    distribution_map = {}
    f = open(file_name)
    file_data_line_by_line = f.read().split('\n')

    file_line_by_line_with_no_monte = []
    monte_data = None
    for line in file_data_line_by_line:
        gaussian = regexParser.parse_guassian_distribution(line)
        monte = regexParser.parse_monte(line)

        if gaussian:
            distribution_map[gaussian[0]] = gaussian[1:]
        if monte:
            monte_data = monte
        else:
            file_line_by_line_with_no_monte.append(line)

    return (file_line_by_line_with_no_monte, distribution_map, monte_data)

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
        
def parse_spice(file_lines, index, distribution_map):
    new_file_lines = []
    for line in file_lines:
        sizing_monte = regexParser.parse_sizing_monte(line)
        if sizing_monte:
            line = calculate_distribution(sizing_monte, index, distribution_map)

        new_file_lines.append(line)
    return new_file_lines 

def generate_process_variation(spice_file):
    result = initial_spice_parse(spice_file)
    lines = result[0]
    distribution_map = result[1]
    if distribution_map == {}:
        return (False, "Distribution not found")
    monte = result[2]
    if monte == None:
        return (False, ".tran XXX XXX sweep monte=XXX didn't found")
    monte_runs = int(monte[2])
    for i in range(monte_runs):
        a = parse_spice(lines, i, distribution_map)
        print('\n'.join(a))

    return (True, "")
    
def main():
    args = handle_args() 
    if args[0] == False:
        print(args[1])
        return
    arg_options = args[1]
    path = utils.get_path_of_input_file(arg_options[__SPICE_FILE])
    print(path)
    generated = generate_process_variation(arg_options[__SPICE_FILE])
    if generated[0] == False:
        print(generated[1])


if __name__ == "__main__":
    main()
