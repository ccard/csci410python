import sys, string, os, io,re
from parser import Parser
from codewriter import CodeWriter

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

#for directories
directory = []
is_dir=False

writer = CodeWriter()

#------------------------------------------------------------------------------
# Check user input
#------------------------------------------------------------------------------
if len(sys.argv) < 1: #Checks to see if user put in file
	print('incorrect number of args!')
	print('assembler.py <file.vm|directry path>')
	sys.exit(0)

in_file=sys.argv[1]

#Checks for correct file name
if re.search('.*\.vm',in_file) is None:
	is_dir=True
	temp = os.listdir(in_file)
	for f in temp:
		if re.search('.*\.vm',f) is not None:
			temp_s = in_file+"/"+f
			directory.append(temp_s)
	
	if len(directory) == 0:
		print("Error no .vm files in path "+in_file)
		sys.exit(0)
else:
	#Strips .asm of the end and adds .hack
	temp_out=re.search('(.*)(\.vm)',in_file)
	out_file+=temp_out.group(1)+'.asm'

#------------------------------------------------------------------------------
# Main
#------------------------------------------------------------------------------

if is_dir:
	for d in directory:
		#Strips .asm of the end and adds .hack
		temp_out=re.search('(.*)(\.vm)',d)
		out_file = temp_out.group(1)+'.asm'

		writer.setFileName(out_file)

		par = Parser(d)
		while par.hasMorecommands():



#---------------------------------End Main-------------------------------------