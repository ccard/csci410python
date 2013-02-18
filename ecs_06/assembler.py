import sys, string, os, io,re
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
# Looks up comp in comp_table if it isn't there reports error and exits
def comp_lookup(comp,line):
	if comp in comp_table:
		return comp_table[comp]
	else:
		print('Unrecognized command '+comp+' on line: '+repr(line)+' !')
		sys.exit(0)

#------------------------------------------------------------------------------
# Looks up dest in dest_table(or extended_dest_table) if it isn't there reports
# error and exits
def dest_lookup(dest,line,extend_dest):
	if dest in dest_table:
		return dest_table[dest]
	else:
		#if we are to look in the extended_dest_table
		if extend_dest:
			if dest in extended_dest_table:
				return extended_dest_table[dest]

		print('Unrecognized destination '+dest+' on line: '+repr(line)+' !')
		sys.exit(0)

#------------------------------------------------------------------------------
# This looks up jump commands and returns the appropriate bit sequence
def jump_lookup(jump,line):
	if jump in jump_table:
		return jump_table[jump]
	else:
		print('Unrecognized jump'+jump+' on line: '+repr(line)+' !')
		sys.exit(0)

#------------------------------------------------------------------------------
# Looks up symbol if it isn't there adds it
def symbol_lookup(sym,line_num,is_label,symbol_table):
	sym=sym.strip('()')
	if sym in symbol_table:
		if is_label:
			bi = bin(line_num) #converts to binary
			bi = bi.lstrip('-0b') #strips -0b of the front
			dif = 16 - len(bi) #calcs number of high order 0's need to make 16bit
			bi = '0'*dif+bi #pads with high order 0's
			symbol_table[sym]=bi

		return symbol_table[sym]

	else:
		if is_label:
			bi = bin(line_num)
			bi = bi.lstrip('-0b')
			dif = 16 - len(bi)
			bi = '0'*dif+bi
			symbol_table[sym]=bi
			return bi

		#user defind variable
		elif re.search('[A-Za-z\_\.\$\:]+[0-9A-Za-z\_\.\$\:]*',sym) is not None:
			bi = 'COUNT' #user def vars 
			symbol_table[sym]='('+sym+')'+bi
			return '('+sym+')'+bi

		else: #explicitly defined variable
			bi = bin(int(sym))
			bi = bi.lstrip('-0b')
			dif = 16 - len(bi)
			bi = '0'*dif+bi
			symbol_table[sym]=bi
			return bi

#------------------------------------------------------------------------------
# This goes through the line and replaces (sym)count with a number and updates 
# table
def user_def_replace(out,symbol_table,user_def):
	original = re.split('\n+',out)
	
	newout=''

	for line in original:
		if len(line) > 0: #ensures that the line is not empty
			if re.search('^\(.*\)COUNT',line) is not None:
				temp_sym = re.search('(^\(.*\))(COUNT)',line)
				#stips symbol out to look up in symbole table
				temp_s = symbol_lookup(temp_sym.group(1),user_def,False,symbol_table)
				#if the returned output contains count
				if re.search('^\(.*\)COUNT',temp_s) is not None:
					#updates the table with the newly assigned registar
					temp = temp_sym.group(1).strip('()')
					bi = bin(user_def)
					bi = bi.lstrip('-0b')
					dif = 16-len(bi)
					bi = '0'*dif+bi
					symbol_table[temp]=bi
					newout+='('+temp+')'+bi+'\n'
					user_def+=1

				else:
					newout+=temp_s+'\n'
			
			else:
				newout+=line+'\n'
	return newout

#------------------------------------------------------------------------------
# Cleans the output of '(sym)'
def clean_out(to_clean):
	listOrig = re.split('\n+',to_clean)

	newOld=''

	for line in listOrig:
		#if it finds (symbol) at the start of line
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
comp_table={'0':'101010','1':'111111','-1':'111010','D':'001100',
			'A':'110000', 'M':'110000', '!D':'001101','!A':'110001',
			'!M':'110001','-D':'001111','-A':'110011', '-M':'110011',
			'D+1':'011111','A+1':'110111', 'M+1':'110111', 'D-1':'001110',
			'A-1':'110010','M-1':'110010','D+A':'000010','D+M':'000010',
			'D-A':'010011', 'D-M':'010011','A-D':'000111', 'M-D':'000111',
			'D&A':'000000','D&M':'000000','D|A':'010101','D|M':'010101'}

dest_table={'null':'000','M':'001','D':'010','MD':'011','A':'100','AM':'101',
			'AD':'110','AMD':'111'}

extended_dest_table={'DM':'011','MA':'101','DA':'110','MDA':'111','DAM':'111',
					'MAD':'111','DMA':'111','ADM':'111'}

jump_table={'null':'000','JGT':'001','JEQ':'010','JGE':'011','JLT':'100',
			'JNE':'101','JLE':'110','JMP':'111'}

symbol_table={'SP':'0000000000000000','LCL':'0000000000000001','ARG':'0000000000000010',
			'THIS':'0000000000000011','THAT':'0000000000000100','R0':'0000000000000000',
			'R1':'0000000000000001','R2':'0000000000000010','R3':'0000000000000011',
			'R4':'0000000000000100','R5':'0000000000000101','R6':'0000000000000110',
			'R7':'0000000000000111','R8':'0000000000001000','R9':'0000000000001001',
			'R10':'0000000000001010','R11':'0000000000001011','R12':'0000000000001100',
			'R13':'0000000000001101','R14':'0000000000001110','R15':'0000000000001111',
			'SCREEN':'0100000000000000','KBD':'0110000000000000'}

user_def_count=16

extended_op=False

in_file=''
out_file=''

#------------------------------------------------------------------------------
# Check user input
#------------------------------------------------------------------------------
if len(sys.argv) < 2: #checks to see if user put in file
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

#------------------------------------------------------------------------------
# Main
#------------------------------------------------------------------------------
IN=open(in_file)

#Builds the symbol table
line_num=0
for line in IN:
	line = line.strip()

	if re.search('^\@.*',line) is not None:
		line = line.lstrip('@')
		toWrite=symbol_lookup(line,line_num,False,symbol_table)
		line_num+=1

	#User deffined variable
	elif re.search('^\(.*\)[0-9]+',line) is not None and extended_op:
		temp_udef = re.search('(^\(.*\))([0-9]+)',line)
		symbol_lookup(temp_udef.group(1),int(temp_udef.group(2)),True,symbol_table)
		line_num+=1

	#If label
	elif re.search('^\(.*\)',line) is not None:
		symbol_lookup(line,line_num,True,symbol_table)

	#If line is a command and not empty
	elif re.search('^\/\/',line) is None and len(line) > 1:
		line_num+=1
#End for loop

IN.close
IN=open(in_file)
OUT=open(out_file,'w')

toWrite=''
output=''
#Keeps track of line number as far as .hack file is concerned
line_num=0
#Keeps count for general error reporting
overall_line_num=0

#Builds the output
for line in IN:
	line = line.strip()

	if re.search('^\@.*',line) is not None:
		line = line.lstrip('@')
		toWrite+=symbol_lookup(line,line_num,False,symbol_table)
		line_num+=1

	#If the line is a label then we just want to ensure that it
	#doesn't get read in as a command and cause an error
	elif re.search('^\(.*\)',line) is not None:
		temp_s='This is here to ensure that labels don`t get printed to output'

	elif re.search('^\/\/',line) is None and len(line) > 1:
		toWrite='111' #Begining of c instruction
		
		#If there is a comment at end of line
		if re.search('.*\/\/.*',line) is not None:
			#Strips comment off
			temp_line = re.search('(.*)(\/\/.*)',line)
			line=temp_line.group(1)
			line=line.strip()

		#If m is involved in the computation sets a to 1
		if re.search('=.*M.*',line) is None:
			toWrite+='0'
		else:
			toWrite+='1'

		#If there is a destination involved
		if re.search('\=',line) is None:
			#If there is a jump involved
			if re.search(';',line) is None:
				toWrite+=comp_lookup(line,overall_line_num)
				toWrite+=dest_lookup('null',overall_line_num,extended_op)
				toWrite+=jump_lookup('null',overall_line_num)
			else:
				temp_jump = re.search('(.*)(;)(.*)',line)
				toWrite+=comp_lookup(temp_jump.group(1),overall_line_num)
				toWrite+=dest_lookup('null',overall_line_num,extended_op)
				toWrite+=jump_lookup(temp_jump.group(3),overall_line_num)
		else:
			#If there is a jump involved
			if re.search(';',line) is None:
				temp_dest=re.search('(.*)(\=)(.*)',line)
				toWrite+=comp_lookup(temp_dest.group(3),overall_line_num)
				toWrite+=dest_lookup(temp_dest.group(1),overall_line_num,extended_op)
				toWrite+=jump_lookup('null',overall_line_num)
			else:
				temp_dest = re.search('(.*)(\=)(.*)(;)(.*)',line)
				toWrite+=comp_lookup(temp_dest.group(3),overall_line_num)
				toWrite+=dest_lookup(temp_dest.group(1),overall_line_num,extended_op)
				toWrite+=jump_lookup(temp_dest.group(5),overall_line_num)
		
		line_num+=1
	
	overall_line_num+=1

	if len(toWrite) > 0:
		output+=toWrite+'\n'
		toWrite=''
#End for loop

IN.close()
output = user_def_replace(output,symbol_table,user_def_count)
output = clean_out(output)
OUT.write(output)
OUT.close()
#---------------------------End Program----------------------------------------