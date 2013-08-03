import os
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('-c','--compare',help='Compares to the baseline. Argument must be the baseline file to be compared to.')
parser.add_argument('-r','--root',help='Specifies the starting root directory')
parser.add_argument('-b','--baseline',help='Sets to record a baseline')
args = parser.parse_args()
print "hello"
startingDirectory = args.root
outputFile = 'baseline.txt'
#Function used to navigate through the directory tree and output each file along with its modification time to a textfile defined by the variable outputFile.
def walk():
    #clears the output file if it previously exists.
    output = open(args.baseline, 'w')
    output.close()
    #iterates through the directory listings
    for root, dirs, files in os.walk(startingDirectory):
        #Iterates through the files
        for file in files:
            filename = root + "\\" + file
            output = open(args.baseline, 'a')
            #Outputs the filename and location along with the creating since epoch to the outputFile.
            output.write(filename + ' > ' + str(os.stat(filename).st_mtime) + '\n')
    output.close()
def compare():
    #Opens the input file for comparison.
    inputFile = open(args.compare, 'r')
    #iterates through the directory listings
    for root, dirs, files in os.walk(startingDirectory):
        #Iterates through the files
        for file in files:
            filename = root + "\\" + file
            #Checks if the current file being observed exists in the inputFile.
            currentPosition = inputFile.tell()
            if inputFile.readline() != filename + ' > ' + str(os.stat(filename).st_mtime) + '\n':
                #Prints the filename / location and modification date if file is new or modified.
                print filename + ' > ' + str(os.stat(filename).st_mtime) + '\n'
                #Skips one line if new file is added.
                inputFile.seek(currentPosition)
def test():
    inputFile = open(args.compare, 'r')
    print inputFile.readline()
    print inputFile.tell()
    print inputFile.readline()
    print inputFile.tell()
if startingDirectory == None:
    #If running a Windows based system
    if os.name == 'nt':
        startingDirectory = 'C:\\'
    #If running a Unix based system.
    else:
        startingDirectory = '.'
print startingDirectory
if args.compare:
    compare()
    #test()
if args.baseline:
    walk()
print 'done'