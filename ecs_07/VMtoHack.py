import sys, string, os, io,re
from parser import Parser

#------------------------------------------------------------------------------
#Chris Card
#CS410
#ECS project 06
#python 3.3
#Due:3/4/13
#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
# Def sub routines
#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
# Cretes push commands
def init_sp():
	temp_s = "@256\n"
	temp_s += "D=A\n\n"
	temp_s += "@sp\n"
	temp_s += "M=D\n\n"
	return temp_s

#------------------------------------------------------------------------------
# Cretes push commands
def push(p_val):
	temp_s += "@"+p_val+"\n"
	temp_s += "D=A\n\n"
	temp_s = "@SP\n"
	temp_s += "A=M\n"
	temp_s += "M=D\n\n"
	temp_s += "@SP\n"
	temp_s += "M=M+1"
	return temp_s

#------------------------------------------------------------------------------
# Cretes pop commands
def pop():



#------------------------------------------------------------------------------
# Var declerations
#------------------------------------------------------------------------------

in_file=''
out_file=''

#------------------------------------------------------------------------------
# Check user input
#------------------------------------------------------------------------------
if len(sys.argv) < 1: #Checks to see if user put in file
	print('incorrect number of args!')
	print('assembler.py <file.asm>')
	sys.exit(0)

in_file=sys.argv[1]

#Checks for correct file name
if re.search('.*\.vm',in_file) == None:
	print('incorrect file name!')
	sys.exit(0)

#Strips .asm of the end and adds .hack
temp_out=re.search('(.*)(\.asm)',in_file)
out_file+=temp_out.group(1)+'.asm'

#------------------------------------------------------------------------------
# Main
#------------------------------------------------------------------------------





#---------------------------------End Main-------------------------------------