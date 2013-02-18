import sys, string, os, io,re
from parser import Parser
from code import Code
from symboltable import SymbolTable
#------------------------------------------------------------------------------
#Chris Card
#CS410
#ECS project 06
#Due:2/25/13
#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
# Def sub routines
#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
# This goes through the line and replaces (sym)count with a number and updates 
# table
def user_def_replace(out,user_def):
	original = re.split('\n+',out)
	
	newout=''

	for line in original:
		if len(line) > 0: #Ensures that the line is not empty
			if re.search('^\(.+\).*',line) is not None:
				temp_sym = re.search('(^\(.*\))(.*)',line)
				#Updates the table with the newly assigned registar
				temp = temp_sym.group(1).strip('()')
				if re.search('\(.*\).*',symT.getAddress(temp)) is not None:
					symT.addEntry(temp,user_def,False)
					newout+='('+temp+')'+symT.getAddress(temp)+'\n'
					user_def+=1
				else:
					newout+=symT.getAddress(temp)+'\n'
			
			else:
				newout+=line+'\n'
	return newout

#------------------------------------------------------------------------------
# Cleans the output of '(sym)'
def clean_out(to_clean):
	listOrig = re.split('\n+',to_clean)

	newOld=''

	for line in listOrig:
		#If it finds (symbol) at the start of line
		if re.search('^\(.*\).*',line) is not None:
			temp = re.search('(^\(.*\))(.*)',line)
			newOld+=temp.group(2)+'\n'
		
		else:
			newOld+=line+'\n'
	
	newOld = newOld.strip('\n')
	return newOld

#------------------------------------------------------------------------------
# Var declerations
#------------------------------------------------------------------------------
user_def_count=16

extended_op=False

in_file=''
out_file=''

#------------------------------------------------------------------------------
# Check user input
#------------------------------------------------------------------------------
if len(sys.argv) < 2: #Checks to see if user put in file
	print('incorrect number of args!')
	print('assembler.py <file.asm> <-x(optional extended mode)>')
	sys.exit(0)

in_file=sys.argv[1]

#Checks for correct file name
if re.search('.*\.asm',in_file) == None:
	print('incorrect file name!')
	sys.exit(0)

#If user passed in option to allow extra functionality
if len(sys.argv) == 3:
	temp_op=sys.argv[2]
	if '-x' in temp_op:
		extended_op=True

#Strips .asm of the end and adds .hack
temp_out=re.search('(.*)(\.asm)',in_file)
out_file+=temp_out.group(1)+'.hack'

par = Parser(in_file,extended_op)
code = Code()
symT = SymbolTable()

#------------------------------------------------------------------------------
# Main
#------------------------------------------------------------------------------

#Builds the symbol table
while par.hasMoreCommands():
	par.advance()
	cType = par.commandType()
	if re.search('L_COMMAND',cType) is not None:
		temp_L = re.search('(.*)(;)(.*)',par.symbol())
		symT.addEntry(temp_L.group(1),int(temp_L.group(3)),False)

	elif re.search('A_COMMAND',cType) is not None:
		if not symT.contains(par.symbol()):
			if re.search('^[0-9]+',par.symbol()) is not None:
				symT.addEntry(par.symbol(),int(par.symbol()),False)
			else:
				symT.addEntry(par.symbol(),user_def_count,True)
	
#End loop


OUT=open(out_file,'w')
par2 = Parser(in_file,extended_op)

toWrite=''
output=''

#Keeps count for general error reporting
overall_line_num=0

#Builds the output
while par2.hasMoreCommands():
	par2.advance()

	if re.search('A_COMMAND',par2.commandType()) is not None:
		toWrite+=symT.getAddress(par2.symbol())

	elif re.search('C_COMMAND',par2.commandType()) is not None:
		toWrite='111' #Begining of c instruction
		
		#If m is involved in the computation sets a to 1
		if re.search('.*M.*',par2.comp()) is None:
			toWrite+='0'
		else:
			toWrite+='1'

		toWrite+=code.comp(par2.comp(),overall_line_num)
		toWrite+=code.dest(par2.dest(),overall_line_num,extended_op)
		toWrite+=code.jump(par2.jump(),overall_line_num)
	
	overall_line_num+=1

	if len(toWrite) > 0:
		output+=toWrite+'\n'
		toWrite=''
#End for loop

output = user_def_replace(output,user_def_count)
output = clean_out(output)
OUT.write(output)
OUT.close()
#---------------------------End Program----------------------------------------