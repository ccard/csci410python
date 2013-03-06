import sys, string, os, io,re
from parser import Parser
from codewriter import CodeWriter

#------------------------------------------------------------------------------
#Chris Card
#CS410
#ECS project 07
#python 3.3
#Due:3/4/13
#This is the main program
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
if_type='C_IF-C_GOTO'
funct_type='C_FUNCTION'
ret_type='C_RETURN'
call_type='C_CALL'

in_file=''
out_file=''

#for directories
directory = []
is_dir=False

#is first time through
is_first=True

#------------------------------------------------------------------------------
# Check user input
#------------------------------------------------------------------------------
if len(sys.argv) < 2: #Checks to see if user put in file
	print('incorrect number of args!')	
	print('assembler.py <file.vm|directry path>')
	sys.exit(0)

in_file=sys.argv[1]

#Checks for correct file name if not then assumes directory
if re.search('.*\.vm',in_file) is None:
	is_dir=True
	#goes through the directory and finds the .vm files
	temp = os.listdir(in_file)
	for f in temp:
		if re.search('.*\.vm',f) is not None:
			temp_s = in_file+"/"+f
			directory.append(temp_s)
	
	#if no files found in directory then error
	if len(directory) == 0:
		print("Error no '*.vm' files in path "+in_file)
		sys.exit(0)
else:
	#Strips .vm of the end and adds .asm
	temp_out=re.search('(.*)(\.vm)',in_file)
	out_file+=temp_out.group(1)+'.asm'

#------------------------------------------------------------------------------
# Main
#------------------------------------------------------------------------------

#for directories passed in
if is_dir:
	cur_dir = os.getcwd()
	temp_dir = re.search('([\/"\\"]{1})([A-Za-z0-9\.\_\-\s]*$)',cur_dir)
	fileName = temp_dir.group(2)+'.asm'
	writer = CodeWriter(cur_dir+'/'+fileName)
	writer.writeInit()
	for d in directory:
		#Strips .vm of the end and adds .asm
		temp_out=re.search('(.*[\.\/]+)(.*)(\.vm)',d)
		out_file = temp_out.group(2)

		#opens the output file
		writer.setFileName(out_file)

		#opens the input file
		par = Parser(d)
		#while not eof
		while par.hasMoreCommands():
			par.advance()
			cType = par.commandType()

			if arith_type in cType:
				writer.writeArithmetic(par.arg_1())
			
			elif push_type in cType:
				if len(par.arg_2()) == 0:
					writer.writePushPop(cType,'constant',par.arg_1())
				else:
					writer.writePushPop(cType,par.arg_1(),par.arg_2())

			elif pop_type in cType:
				if len(par.arg_2()) == 0:
					writer.writePushPop(cType,'constant',par.arg_1())
				else:
					writer.writePushPop(cType,par.arg_1(),par.arg_2())

			elif funct_type in cType:
				print('this is funct '+par.arg_1()+' with # arg'+par.arg_2())
				writer.writeFunction(par.arg_1(),par.arg_2())

			elif if_type in cType:
				writer.writeIf(par.arg_1())

			elif goto_type in cType:
				writer.writeGoto(par.arg_1())

			elif lable_type in cType:
				writer.writeLabel(par.arg_1())

			elif call_type in cType:
				writer.writeCall(par.arg_1(),par.arg_2())

			elif ret_type in cType:
				writer.writeReturn()

	writer.Close()

#this is for a single file
else:
	writer = CodeWriter(out_file)
	writer.writeInit()
	writer.setFileName(out_file)


	par = Parser(in_file)
	while par.hasMoreCommands():
		par.advance()
		cType = par.commandType()

		if arith_type in cType:

			writer.writeArithmetic(par.arg_1())
		
		elif push_type in cType:
			if len(par.arg_2()) == 0:
				writer.writePushPop(cType,'constant',par.arg_1())
			else:
				writer.writePushPop(cType,par.arg_1(),par.arg_2())

		elif pop_type in cType:
			if len(par.arg_2()) == 0:
				writer.writePushPop(cType,'constant',par.arg_1())
			else:
				writer.writePushPop(cType,par.arg_1(),par.arg_2())

		elif funct_type in cType:
			writer.writeFunction(par.arg_1(),par.arg_2())

		elif if_type in cType:
			writer.writeIf(par.arg_1())

		elif goto_type in cType:
			writer.writeGoto(par.arg_1())

		elif lable_type in cType:
			writer.writeLabel(par.arg_1())

		elif call_type in cType:
			writer.writeCall(par.arg_1(),par.arg_2())

		elif ret_type in cType:
			writer.writeReturn()

	writer.Close()


#---------------------------------End Main-------------------------------------