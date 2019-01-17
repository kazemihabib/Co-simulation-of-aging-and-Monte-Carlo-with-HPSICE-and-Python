import sys, os
import subprocess

def get_path_to_generate_temp_data(input_file):
    path = os.path.dirname(input_file)        
    return os.path.abspath(os.path.join(path, "toolchain"))

def create_directory(dir, path):
    directory = os.path.join(path, dir)
    if not os.path.exists(directory):
        os.makedirs(directory)
    return directory

def write_to_file(filename, file_index, path, data_list):
    directory = create_directory(filename+str(file_index), path)
    file_path = os.path.join(directory, filename) 

    f = open(file_path, 'w')
    f.writelines('\n'.join(data_list))

    return file_path

def run_hspice(file_path):
    test = subprocess.Popen(["hspice", '-i', file_path, '-o', '/'.join(file_path.split('/')[:-1]), '-mt', '8'], stdout=subprocess.PIPE)
    output = test.communicate()[0]
    print(output)
