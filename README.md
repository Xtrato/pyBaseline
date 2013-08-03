This scripts has been created to be used during malware analysis. It takes a baseline of files and folders present on the system. Once the malware is executed it can be used to compare any changes made to the system.

Usage
    usage: pyBaseline.py [-h] [-c COMPARE] [-r ROOT] [-b BASELINE]

    optional arguments:
      -h, --help            show this help message and exit
      -c COMPARE, --compare COMPARE
                            Compares to the baseline Argument must be the baseline
                            file to be compared to.
      -r ROOT, --root ROOT  Specifies the starting root directory
      -b BASELINE, --baseline BASELINE
                            Sets to record a baseline

Examples:

To take a baseline of the system and save the results to the file baseline.txt

        pyBaseline.py -b baseline.txt

To specify a starting directory use the -r tag. By default it scans the whole drive.

        pyBaseline.py -r C:\Users\Name -b baseline.txt

To compare the current system with the previously recorded results stored in baseline.txt.

        pyBaseline.py -c baseline.txt