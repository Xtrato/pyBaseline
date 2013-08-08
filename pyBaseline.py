import os
import argparse
import re
parser = argparse.ArgumentParser()
parser.add_argument('-c','--compare',help='Compares to the baseline. Argument must be the baseline file to be compared to.')
parser.add_argument('-r','--root',help='Specifies the starting root directory')
parser.add_argument('-b','--baseline',help='Sets to record a baseline')
args = parser.parse_args()
startingDirectory = args.root
outputFile = 'baseline.txt'
#Function used to navigate through the directory tree and output each file along with its modification time to a textfile defined by the variable outputFile.
if startingDirectory == None:
    #If running a Windows based system
    if os.name == 'nt':
        startingDirectory = 'C:\Fraps'
        seperator = '\\'
    #If running a Unix based system.
    else:
        startingDirectory = '.'
        seperator = '/'
if args.compare:
    filesAdded = 0
    filesModified = 0
    print '[*] Comparing current system files and folders against ' + args.compare + '.'
    #Opens the input file for comparison.
    inputFile = open(args.compare, 'r')
    #iterates through the directory listings
    for root, dirs, files in os.walk(startingDirectory):
        #Iterates through the files
        for file in files:
            filename = root + seperator + file
            #Keeps track of inputFile read location. Used if a file or folder has changed.
            currentPosition = inputFile.tell()
            #Checks if the current file being observed exists in the inputFile.
            if inputFile.readline() != filename + ' > ' + str(os.stat(filename).st_mtime) + '\n':
                #If only the filename is the same but the modification time has changed.
                inputFile.seek(currentPosition)
                if inputFile.readline()[:re.search('>', inputFile.readline()).start()] == filename:
                    filesModified = filesModified + 1
                    #Prints the filename / location and modification date if file is new or modified.
                    print filename + ' > ' + str(os.stat(filename).st_mtime) + '\n'
                else:
                    filesAdded = filesAdded + 1
                    #Prints the filename / location and modification date if file is new or modified.
                    print filename + ' > ' + str(os.stat(filename).st_mtime) + '\n'
            #Skips one line back if new file is added.
            inputFile.seek(currentPosition)
    print '[*] Found ' + str(filesAdded) + ' new files and ' + str(filesModified) + ' files altered'
if args.baseline:
    print '[*] Scanning files and folders'
    #clears the output file if it previously exists.
    output = open(args.baseline, 'w')
    output.close()
    #iterates through the directory listings
    for root, dirs, files in os.walk(startingDirectory):
        #Iterates through the files
        for file in files:
            filename = root + seperator + file
            output = open(args.baseline, 'a')
            #Outputs the filename and location along with the modification time since epoch to the outputFile.
            output.write(filename + ' > ' + str(os.stat(filename).st_mtime) + '\n')
    print '[*] Outputting directory structure to ' + args.baseline
    output.close()
    print '[*] ' + args.baseline + ' saved'
    print '[*] Scan Complete'