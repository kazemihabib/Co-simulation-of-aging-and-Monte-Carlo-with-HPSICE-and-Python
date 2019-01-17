import sys, os

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

    f = open(os.path.join(directory, filename),'w')
    f.writelines('\n'.join(data_list))


