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
# Var declerations
#------------------------------------------------------------------------------

#Constance
arith_type='C_ARITHMETIC'
push_type='C_PUSH'
pop_type='C_POP'
lable_type='C_LABEL'
goto_type='C_GOTO'
if_type='C_IF'
funct_type='C_FUNCTION'
ret_type='C_RETURN'
call_type='C_CALL'

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