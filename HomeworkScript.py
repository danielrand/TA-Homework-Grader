import argparse
import errno
import imaplib
import os
import email
import shlex
import subprocess
from zipfile import ZipFile
from timeout import TimeoutError, timeout
# Configuring Run Variables based on command line args and user input email info
parser = argparse.ArgumentParser()
parser.add_argument('-target','-t', type=str, required=True, help = 'Project Directory')
parser.add_argument('--inFiles', "-i", type=str, required = True, nargs='+',
                    help='an integer for the accumulator')
parser.add_argument('-numOutFiles', "-o", type=int, required=True, help='Number of outfiles')
parser.add_argument('-language', "-l", type=str, required=True, help='Coding Language')
username = raw_input('Username: ')
password = raw_input('Password: ')
directory = parser.parse_args().target
projectInput = raw_input('Search string for project: ')
language = parser.parse_args().language
data = parser.parse_args().inFiles
num_out_files = parser.parse_args().numOutFiles

print ("\nSearching inbox for " + projectInput + "...\n")

# Get most recent 100 emails
def get_most_recent_emails(messages):
    # Getting in most recent emails
    ids = messages[0]  # data is a list.
    id_list = ids.split()  # ids is a space separated string
    # latest_ten_email_id = id_list  # get all
    latest_ten_email_id = id_list[-500:]  # get the latest 500
    keys = map(int, latest_ten_email_id)
    news_keys = sorted(keys, reverse=True)
    str_keys = [str(e) for e in news_keys]
    return str_keys


mail = imaplib.IMAP4_SSL("imap.gmail.com", 993)
mail.login(username, password)
mail.select()
mail.select()
(retcode, messages) = mail.search(None, 'ALL')
news_mail = get_most_recent_emails(messages)
reachedSpecs = False
# Search email
for i in news_mail:
    if reachedSpecs: break
    typ, email_data = mail.fetch(i, '(RFC822)')
    raw_email = email_data[0][1]
    raw_email_string = raw_email.decode('utf-8')
    try:
        email_message = email.message_from_string(raw_email_string)
    except Exception as e:
        continue
    for part in email_message.walk():
        if part.get_content_maintype() == 'multipart':
            continue
        if part.get('Content-Disposition') is None:
            continue
        subjectString = str(email_message).split("Subject: ", 1)[1].split("\nTo:", 1)[0]
        subject = subjectString.lower().replace(" ", "")
        project = projectInput.lower().replace(" ", "")
        if project not in subject:
            continue
        fileName = part.get_filename()
        if bool(fileName):
            filePath = os.path.join(directory, fileName)
            if not os.path.isfile(filePath):
                fp = open(filePath, 'wb')
                fp.write(part.get_payload(decode=True))
                fp.close()
            print('Downloaded "{file} received on "{date}"'.format(file=fileName, date = email_message['Date']))
            #if '.doc' in fileName: reachedSpecs = True

print ("\nPREPARING TO RUN CODE...\n\n")
raw_input("\nMake sure to make input files read only! Type any key and press enter to continue after doing so:\n")


@timeout(10, os.strerror(errno.ETIMEDOUT))
def run_code(code, data, output_files):
    if language == 'C++':
        compile_command = 'g++ -std=c++11 ' + code
        args = shlex.split(compile_command)
        try:
            subprocess.check_output(args)
        except subprocess.CalledProcessError:
            print ('program did not compile')
            return
    data_files_string = ""
    for string in data:
        data_files_string += string + " "
    if language == 'C++':
        compile_command = './a.out ' + data_files_string
    else:
        compile_command = 'java -jar ' + code + ' ' + data_files_string
    for out_file in output_files:
        compile_command += ' ' + out_file
    args = shlex.split(compile_command)
    try:
        output = subprocess.check_output(args)
    except subprocess.CalledProcessError:
        print ('program did not work:')


def create_output_file(file_path):
    if not os.path.isfile(file_path):
        fp = open(file_path, 'wb')
        fp.close()


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


def run(filename, output_folder, code_path, data):
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
    if file_extension == '.cpp' or (file_extension == '.zip' and language == 'Java'):
        run(filename, output_folder, code_path, data)
    elif os.path.isdir(code_path):
        for subdir, dirs, files in os.walk(code_path):
            for f in files:
                print os.path.join(subdir, f)
                name, file_extension = os.path.splitext(f)
                if file_extension == '.cpp' or (file_extension == '.zip' and language == 'Java'):
                    run(filename, output_folder, os.path.join(subdir,f), data)


def extract_sources_from_zip(directory, file_name):
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


if language == 'C++':
    for filename in os.listdir(directory):
        name, file_extension = os.path.splitext(os.path.join(directory,filename))
        if file_extension == '.zip':
            extract_sources_from_zip(directory, filename)

# to run code
for filename in os.listdir(directory):
    process_file(directory, filename)

    # TODO: ADD ERROR OUTPUT TO SUBMISSION OUTPUT REPORT
    # TODO: ADD DATE AND TIME OF SUBMISSION TO OUTPUT REPORT
    # TODO: ADD Optional just run or just download params
