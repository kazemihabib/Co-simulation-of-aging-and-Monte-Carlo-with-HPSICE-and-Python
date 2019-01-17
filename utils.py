import sys, os

def get_path_of_input_file(input_file):
    pathname = os.path.dirname(input_file)        
    return os.path.abspath(pathname)