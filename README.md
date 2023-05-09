A script for taking a bunch of user/password files and converting them into two master lists -- uname.txt and passwd.txt. This script can be stopped mid-run, and will not read over completed text files listed in status.txt. 

To operate properly, run this script in a directory, and it will read .txt files for user/pass combos, separating credentials to be used in other software.

The script is currently designed to read through the current directory and any accessable subdirectories. This functionality can be changed by altering the logic around line 50.

status.txt example:
foo.txt
bar.txt
baz.txt

To do:
Verbose flag // log file to hold output?
Terminal and init functions to gracefully stop and pick up again
Option to skip redundant passwords
      but how do we do this without taking 200 years?
