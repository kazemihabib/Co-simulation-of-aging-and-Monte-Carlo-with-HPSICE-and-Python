import sys
import regexParser

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

def fill_distribution(line):
    pass
    
def parse_spice(spice_file):
    # file_data_line_by_line = initial_spice_parse(spice_file)
    # for line_index, line in enumerate(file_data_line_by_line):
    #     if '#' in line:
    #         print(line, line_index)
    print("HELLO")

def generate_process_variation(spice_file):
    result = initial_spice_parse(spice_file)
    print(result[0])
    print(result[1])
    print(result[2])
    monte_runs = int(result[2][2])
    for i in range(monte_runs):
        parse_spice(spice_file)
    
def main():
    args = handle_args() 
    if args[0] == False:
        print(args[1])
        return
    arg_options = args[1]
    
    # result = import_scripts(arg_options[__SCRIPT_FILE])
    # print(result[1])
    # if result[0] == False:
    #     return
    
    generate_process_variation(arg_options[__SPICE_FILE])

if __name__ == "__main__":
    main()
