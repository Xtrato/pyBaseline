import os
import argparse
import re
from colorama import init, Fore
init()
print('This tool is used during dynamic analysis of malware.\n It records a baseline of the systems files and folders which can be compared to after the malware has been executed.\n Please use the -h to view the available arguments.\n Modified files are shown in green text\n New files are shown in red text.')
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
        startingDirectory = 'C:\\'
    #If running a Unix based system.
    else:
        startingDirectory = '.'
if os.name == 'nt':
    seperator = '\\'
else:
    seperator = '/'
if args.compare:
    filesAdded = 0
    filesModified = 0
    print '[*] Comparing current system files and folders against ' + args.compare + '.'
    #Opens the input file for comparison.
    inputFile = open(args.compare, 'r')
    #startingDirectory = inputFile.readline()
    startingDirectory = 'C:\Fraps'
    #iterates through the directory listings
    for root, dirs, files in os.walk(startingDirectory):
        #Iterates through the files
        for file in files:
            filename = root + seperator + file
            #Keeps track of inputFile read location. Used if a file or folder has changed.
            currentPosition = inputFile.tell()
            currentLine = inputFile.readline()
            #Checks if the current file being observed exists in the inputFile.
            if currentLine != filename + ' > ' + str(os.stat(filename).st_mtime) + '\n':
                #If only the filename is the same but the modification time has changed.
                if currentLine[:re.search('>', currentLine).start() - 1] == filename:
                    filesModified = filesModified + 1
                    #Prints the filename / location and modification date if file is new or modified.
                    print(Fore.GREEN + filename + ' > ' + str(os.stat(filename).st_mtime))
                    print(Fore.RESET)
                else:
                    filesAdded = filesAdded + 1
                    #Prints the filename / location and modification date if file is new or modified.
                    print(Fore.RED + filename + ' > ' + str(os.stat(filename).st_mtime))
                    print(Fore.RESET)
                    #Skips one line back if new file is added.
                    inputFile.seek(currentPosition)
    print '[*] Found ' + str(filesAdded) + ' new files and ' + str(filesModified) + ' files altered'
if args.baseline:
    print '[*] Scanning files and folders'
    #clears the output file if it previously exists.
    output = open(args.baseline, 'w')
    output.close()
    output = open(args.baseline, 'a')
    #output.write(startingDirectory + '\n')
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