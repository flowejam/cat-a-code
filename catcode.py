#!/usr/bin/env python3
# catcode.py

import os
from collections import deque
from typing import List, TextIO

## TODO: add exception handling
## TODO: add support for appending to a file

class NoSuchDirectoryException(Exception):
    pass

class BadFileTypeFormat(Exception):
    pass


def catcode(file_type: str, directory: str, output_file_name: str, comment_str: str='#') -> TextIO:
    '''
    Purpose: given an extension type (i.e., .py, .c etc.), concatenate
    all files in the given folder, and any subfolders that exist. 

    Writes the output to a file of type 'file_type'.
    '''
    if file_type[0] == '.':
        raise BadFileTypeFormat
    elif output_file_name.endswith('.' + file_type):
        raise BadFileTypeFormat

    output_data = concat_code_files(file_type, directory, comment_str)
    output_file = output_file_name + '.' + file_type 

    with open(output_file, 'w') as f:
        f.write(output_data)

    print(f'Success! Your concatenated code is in {output_file}.')

    

def concat_code_files(file_type: str, directory: str, comment_str: str='#') -> str:
    '''
    Purpose: given an extension type (i.e., .py, .c etc.), concatenate
    all files in the given folder, and any subfolders that exist. 

    Returns a string with the contents of each file concatenated and separated by 
    filename.

    '''
    # TODO: add better comment string handling 

    dir_queue = deque([directory])

    # output string containing concatenated code files
    output_concat_code = ''

    while len(dir_queue) != 0:
        dir_to_process = dir_queue.pop()
        files, directories = get_dirs_and_file_type_matches(file_type, dir_to_process)
        for a_directory in directories:
            dir_queue.appendleft(a_directory)
        output_concat_code += process_code_files(files, comment_str)

    return output_concat_code


def get_dirs_and_file_type_matches(file_type: str, directory: str) -> List[str]:

    if not os.path.isdir(directory):
        raise NoSuchDirectoryException

    path_name = directory
    list_of_files_in_dir = os.listdir(directory)

    files_of_file_type = []
    sub_dirs = []

    for a_file in list_of_files_in_dir:
        new_path = os.path.join(path_name, a_file)
        if os.path.isdir(new_path):
            sub_dirs.append(new_path)
        elif a_file.endswith('.' + file_type):
            files_of_file_type.append(new_path)

    return (files_of_file_type, sub_dirs)


def process_code_files(file_paths: str, comment_str: str) -> str:
    '''
    Returns true if the given file name has the extension of type file_type.
    '''
    output_str = ''
    for file_path in file_paths:
        file_metadata = get_file_metadata(file_path) 
        beginning_str = 2*comment_str + ' ' + file_metadata + 2*'\n'
        ending_str = 2*'\n'
        output_str_for_file = file_metadata
        with open(file_path, 'r') as f:
            data = f.read()
            output_str += (beginning_str + data + ending_str)
    return output_str

def get_file_metadata(file_path: str) -> str:
    ## TODO: provide more details
    return file_path
        


## ========================
def main(argv):
    
    if len(argv) not in (4,5):
        raise SystemExit(f'Error: arguments are as follows: {argv[0]} ' + 'file_type directory_name output_file_name(without extension)')

    #TODO: alter functionality based on optional arguments 
    catcode(argv[1],argv[2],argv[3])


if __name__ == '__main__':
    import sys
    main(sys.argv)
