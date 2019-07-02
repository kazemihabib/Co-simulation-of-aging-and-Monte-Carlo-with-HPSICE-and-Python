import sys, os
import subprocess
import regexParser

def get_path_to_generate_step_data(input_file, step):
    path = os.path.dirname(input_file)        
    step_path = os.path.join(path, "toolchain")
    return os.path.abspath(os.path.join(step_path, "step" + str(step)))

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

    return directory 

def run_hspice(file_path):
    command = ["hspice", '-i', file_path, '-o', '/'.join(file_path.split('/')[:-1]), '-mt', '8']
    # test = subprocess.Popen(, stdout=subprocess.PIPE)
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    # out, error = test.communicate()
    # print(out, error)
    # print(result.returncode, result.stdout, result.stderr)
    print(result.stderr)
    return regexParser.parse_jobs(result.stderr)

def remove_aging_part(fileContent):
    (first, second, third) = regexParser.parse_aging_part(fileContent)
    return (first, second, third) 

def add_aging_part(file_lines, aging_part):
    (first, second, third) = regexParser.parse_aging_part('\n'.join(file_lines))
    return first + '\n' + aging_part + '\n' + third

