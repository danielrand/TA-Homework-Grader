import argparse
# Testing potential argument parsing features
parser = argparse.ArgumentParser()
parser.add_argument('-target','-t', type=str, required=True, help = 'Project Directory')
parser.add_argument('--inFiles', "-i", type=str, required = True, nargs='+',
                    help='an integer for the accumulator')
parser.add_argument('-numOutFiles', "-o", type=int, required=True, help='Number of outfiles')
parser.add_argument('-language', "-l", type=str, required=True, help='Coding Language')

lang = parser.parse_args().language
target = parser.parse_args().target
data = parser.parse_args().inFiles
num_out = parser.parse_args().numOutFiles
print ("Target: " + target)
print ("Data:")
for file in data:
    print (file)
print ("Num out: " + str(num_out))
print ("Language: " + lang)