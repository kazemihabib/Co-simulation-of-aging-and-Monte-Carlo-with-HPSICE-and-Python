import sys, os
import subprocess
import regexParser
import csv
import io
import shutil

def get_path_to_generate_step_data(input_file, step):
    path = os.path.dirname(input_file)        
    step_path = os.path.join(path, "toolchain")
    return os.path.abspath(os.path.join(step_path, "step" + str(step)))

def remove_dir_recursive(dir):
    if os.path.exists(dir):
        shutil.rmtree(dir) 

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
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    # print(result.stderr)
    return regexParser.parse_jobs(result.stderr)

def remove_aging_part(fileContent):
    (first, second, third) = regexParser.parse_aging_part(fileContent)
    return (first, second, third) 

def add_aging_part(file_lines, aging_part):
    (first, second, third) = regexParser.parse_aging_part('\n'.join(file_lines))
    return first + '\n' + aging_part + '\n' + third

def read_csv(file_path):
    with open(file_path, mode='r') as csv_file:
        lines = csv_file.readlines()
        # just keep the columns names and last line
        str_lines = '\n'.join([lines[3], lines[-1]])
        csv_reader = csv.DictReader(io.StringIO(str_lines))

        for row in csv_reader:
            return row

        # print(variables_dict)
        # print(my_dict)
        # print(f'Processed {line_count} lines.')
