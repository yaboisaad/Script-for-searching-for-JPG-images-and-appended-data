Author: Mohammad Saad
CFRS 510
11/19/2020

To execute the program named: hw3Saad.py
you will need to have the following 
modules installed:

os
hashlib
datetime
base64

After these are isntalled, you may execute
the program by typing: 'python hw3Saad.py'
in the command prompt or terminal.

When the program is running, you must enter
a directory that you want to investigate.
An example would be: 'File2Check'
That folder contains other folders and files
that are meant to be checked to see if they
are JPG images or not. The program will also
check to see if any of those files contain
appended data that is encrypted in base64.

The program will create a text file named:
'SaadOutput.txt'
That file will be saved in the same directory
as the one that the program is being executed.
Inside the text file, you will find the names
of the files that are JPGs, their creation,
modification, and access times as well as 
their hashes in sha256. If they happen to 
have any appended data in them, the text file
will contain the decrypted data and the names
of the files that have it. All of the files'
information is stored into a dictionary
and then written into the text file. This is
to keep everything organized.