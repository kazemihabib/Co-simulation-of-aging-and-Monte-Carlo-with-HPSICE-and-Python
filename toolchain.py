import sys

scripts = None
dist_map = None

def parse_file():
    print("HELLO")

def import_scripts(scripts_file):
    scripts = __import__(scripts_file)
    try:
        distribution_map = getattr(scripts, "distibution_map")
    except: 
        return (False, "No distribution dictionary defined")
    else:
        print(distribution_map)
    
    return (True, 'Parsed the module "{0}" succesfully'.format(scripts_file))

def handle_args():
    args = sys.argv
    print(args)
    message = "The correct way to this program is: python3 toolchain.py -i yourspicefile.sp -s yourscripts.py "
    if len(args) < 5:
        return (False, message)

    cont = True 
    arg_dict = {}
    SPICE_FILE = "spice_file"
    SCRIPT_FILE = "script_file"
    for i in range(len(args)):
        if cont == True:
            cont = False
            continue

        if args[i] == '-i':
            arg_dict[SPICE_FILE] = args[i+1]
            cont == True
        elif args[i] == "-s":
            arg_dict[SCRIPT_FILE] = args[i+1].split('.')[0] #remove .py
            cont = True

    if SPICE_FILE not in arg_dict or SCRIPT_FILE not in arg_dict:
        return (False, message)

    return (True, arg_dict)

def main():
    args = handle_args() 
    if args[0] == False:
        print(args[1])
        return
    arg_options = args[1]
    
    result = import_scripts(arg_options["script_file"])
    print(result[1])
    if result[0] == False:
        return

if __name__ == "__main__":
    main()
