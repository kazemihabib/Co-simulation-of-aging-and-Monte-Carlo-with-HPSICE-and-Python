import sys

scripts = None
dist_map = None
runs = None
__SPICE_FILE = "spice_file"
__SCRIPT_FILE = "script_file"

def parse_file():
    print("HELLO")

def import_scripts(scripts_file):
    global scripts, dist_map, runs
    scripts = __import__(scripts_file)
    try:
        distribution_map = getattr(scripts, "distibution_map")
        runs = getattr(scripts, "runs")
    except: 
        return (False, "No distribution dictionary defined")
    else:
        print(distribution_map)
    
    return (True, 'Parsed the module "{0}" succesfully'.format(scripts_file), )

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

def read_file(file_name):
    f = open(file_name)
    file_data = f.read()
    file_data_line_by_line = file_data.split('\n')
    return file_data_line_by_line

def fill_distribution(line):
    
def parse_spice(spice_file):
    file_data_line_by_line = read_file(spice_file)
    for line_index, line in enumerate(file_data_line_by_line):
        if '#' in line:
            print(line, line_index)

def generate_process_variation(spice_file, runs):
    for i in range(runs):
        parse_spice(spice_file)
    
def main():
    args = handle_args() 
    if args[0] == False:
        print(args[1])
        return
    arg_options = args[1]
    
    result = import_scripts(arg_options[__SCRIPT_FILE])
    print(result[1])
    if result[0] == False:
        return
    
    generate_process_variation(arg_options[__SPICE_FILE], runs)

if __name__ == "__main__":
    main()
