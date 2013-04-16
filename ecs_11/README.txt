Instructions:

To run full compiler:
python JackCompiler.py <directory|file>
Output will be sent to the same directory as the file or directory you passed in

NOTE: for testing convert to binary do the following
open Main.vm in the convert to binary directory
and do the following:

Change the first 4 lines of the file looking like the below
function Main.main 2
push constant 8001
push constant 16
push constant 1

to:
function Main.main 2
push constant 8000
pop pointer 1
push constant 32
pop that 0
push constant 8001
push constant 16
push constant 1


To run just the xml option:
python JackCompiler.py -x <directory|file>
Output will be sent to the same directory as the file or directory you passed in