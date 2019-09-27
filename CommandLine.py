import errno
import subprocess, os, shlex
from zipfile import ZipFile
from timeout import timeout, TimeoutError
# Data File 1: /Users/danielrand/Desktop/Queens_College_Classes/CS323_35(TA)/Bucket/BucketSort_Data.txt
#/Users/danielrand/Desktop/Queens_College_Classes/CS323_35(TA)/Bucket
# directory = "/Users/danielrand/Desktop/Queens_College_Classes/CS323_35(TA)/Proj3";
# data = '/Users/danielrand/Desktop/Queens_College_Classes/CS323_35(TA)/Proj3/HuffmanTreeCoding_Data.txt'
language = raw_input("Coding language: ")
data = []
i = 1
num_in_files_string = raw_input("Number of input files: ")
num_in_files = int(num_in_files_string)

while i <= num_in_files:
    data.append(raw_input("Data File " + str(i) + ": "))
    i += 1
numString = raw_input("Number of output files: ")
num_out_files = int(numString)
directory = raw_input("Project Directory: ")

def create_output_file(file_path):
    if not os.path.isfile(file_path):
        fp = open(file_path, 'wb')
        fp.close()

@timeout(10, os.strerror(errno.ETIMEDOUT))
def run_code(code, data, output_files):
    compile_command = 'g++ ' + code
    args = shlex.split(compile_command)
    try:
        subprocess.check_output(args)
    except subprocess.CalledProcessError:
        print ('program did not compile')
        return
    data_files_string = ""
    for string in data:
        data_files_string += string + " "
    compile_command = './a.out ' + data_files_string
    for out_file in output_files:
        compile_command += ' ' + out_file
    args = shlex.split(compile_command)
    try:
        output = subprocess.check_output(args)
    except subprocess.CalledProcessError:
        print ('program did not work:')


def process_out_files(filename, output_folder, fileNm):
    print('Processing ' + filename)
    i = 1
    output_files = []
    while i <= num_out_files:
        output_file = os.path.join(output_folder, fileNm + '_outFile' + str(i) + '.txt')
        create_output_file(output_file)
        output_files.append(output_file)
        i += 1
    return output_files


def extract_sources_from_zip (directory, file_name):
    print ('Extracting ' + filename)
    file = os.path.join(directory, file_name)
    with ZipFile(file, 'r') as zip:
        # printing all the contents of the zip file
        zip.printdir()
        #Creating the Sumbission Folder
        folder = file + '_Code'
        if not os.path.isdir(folder):
            os.makedirs(folder)
        # extracting all the files
        print('Extracting all the files now...')
        zip.extractall(folder)
        print('Done!')
        print('Contents:')

def run (filename, output_folder, code_path, data):
    output_files = process_out_files(filename, output_folder, filename)
    try:
        run_code(code_path, data, output_files)
    except TimeoutError:
        print ("INFINITE LOOP")

def process_file(dir, fileNm):
    code_path = os.path.join(dir, fileNm)
    name, file_extension = os.path.splitext(code_path)
    output_folder = os.path.join(directory,'Output')
    if not os.path.isdir(output_folder):
        os.makedirs(output_folder)
    if file_extension == '.cpp':
        run(filename,output_folder,code_path,data)
    elif os.path.isdir(code_path):
        for subdir, dirs, files in os.walk(code_path):
            for f in files:
                print os.path.join(subdir, f)
                name, file_extension = os.path.splitext(f)
                if file_extension == '.cpp':
                    run(filename, output_folder, os.path.join(subdir,f), data)


if language == 'C++':
    for filename in os.listdir(directory):
        name, file_extension = os.path.splitext(os.path.join(directory,filename))
        if file_extension == '.zip':
            extract_sources_from_zip(directory, filename)

# to run code
for filename in os.listdir(directory):
    process_file(directory, filename)