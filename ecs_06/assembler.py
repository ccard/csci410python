import sys, string, os, io,re
#Chris Card
#CS410
#Python02
#due:2/6/13

#------------------------------------------------------------------------------
#DEF sub routines
#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
#Looks up comp in comp_table if it isn't there reports error and exits
def comp_lookup(comp):
	if comp in comp_table:
		return comp_table[comp]
	else:
		print('Unrecognized command '+comp+' !')
		sys.exit(0)

#------------------------------------------------------------------------------
#Looks up dest in dest_table if it isn't there reports error and exits
def dest_lookup(dest):
	if dest in dest_table:
		return dest_table[dest]
	else:
		print('Unrecognized destination '+dest+' !')
		sys.exit(0)

#------------------------------------------------------------------------------
#This looks up jump commands and returns the appropriate bit sequence
def jump_lookup(jump):
	if jump in jump_table:
		return jump_table[jump]
	else:
		print('Unrecognized jump'+jump+' !')
		sys.exit(0)

#------------------------------------------------------------------------------
#looks up symbol if it isn't there adds it
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

		elif re.search('[A-Za-z\_\.\$\:]+[0-9A-Za-z\_\.\$\:]*',sym) is not None:
			bi = 'COUNT' #user def vars 
			symbol_table[sym]='('+sym+')'+bi
			return '('+sym+')'+bi

		else:
			bi = bin(int(sym))
			bi = bi.lstrip('-0b')
			dif = 16 - len(bi)
			bi = '0'*dif+bi
			symbol_table[sym]=bi
			return bi

#------------------------------------------------------------------------------
#This goes through the line and replaces (sym)count with a number and updates table
def user_def_replace(out,symbol_table,user_def):
	original = re.split('\n+',out)
	
	newout=''
	#count for assigning registars to user def vars
	repeat = 0

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
					print(temp+':'+repr(user_def))
					repeat+=1
					user_def+=1
					if repeat == 2:
						user_def=16
						repeat=0
				else:
					newout+=temp_s+'\n'
			else:
				newout+=line+'\n'
	return newout

#------------------------------------------------------------------------------
#cleans the output of (sym)
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
#Var declerations
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

in_file=''
out_file=''

#------------------------------------------------------------------------------
#Check user input
#------------------------------------------------------------------------------
if len(sys.argv) < 2: #checks to see if user put in file
	print('incorrect number of args!')
	print('assembler.py <file.asm>')
	sys.exit(0)

in_file=sys.argv[1]

#checks for correct file name
if re.search('.*\.asm',in_file) == None:
	print('incorrect file name!')
	sys.exit(0)

#strips asm of the end and adds hack
out_file=in_file.rstrip('.asm')
out_file+='.hack'

#------------------------------------------------------------------------------
#Main
#------------------------------------------------------------------------------
IN=open(in_file)

#builds the symbol table
line_num=0
for line in IN:
	line = line.strip()

	if re.search('^\@.*',line) is not None:
		line = line.lstrip('@')
		toWrite=symbol_lookup(line,line_num,False,symbol_table)
		line_num+=1

	elif re.search('^\(.*\)',line) is not None:
		symbol_lookup(line,line_num,True,symbol_table)

	elif re.search('^\/\/',line) is None and len(line) > 1:
		line_num+=1
#end for loop

IN.close
IN=open(in_file)
OUT=open(out_file,'w')

toWrite=''
output=''
line_num=0
#builds the output
for line in IN:
	line = line.strip()

	if re.search('^\@.*',line) is not None:
		line = line.lstrip('@')
		toWrite+=symbol_lookup(line,line_num,False,symbol_table)
		line_num+=1

	elif re.search('^\(.*\)',line) is not None:
		temp_s='This is here to ensure that labels don`t get printed to output'

	elif re.search('^\/\/',line) is None and len(line) > 1:
		toWrite='111' #command begining
		
		#if there is a comment in middle or end of line
		if re.search('.*\/\/.*',line) is not None:
			#strips comment off
			temp_line = re.search('(.*)(\/\/.*)',line)
			line=temp_line.group(1)
			line=line.strip()

		#if m is involved in the computation sets a to 1
		if re.search('=.*M.*',line) is None:
			toWrite+='0'
		else:
			toWrite+='1'

		#if there is a destination involved
		if re.search('\=',line) is None:
			#if there is a jump involved
			if re.search(';',line) is None:
				toWrite+=comp_lookup(line)
				toWrite+=dest_lookup('null')
				toWrite+=jump_lookup('null')
			else:
				temp_jump = re.search('(.*)(;)(.*)',line)
				toWrite+=comp_lookup(temp_jump.group(1))
				toWrite+=dest_lookup('null')
				toWrite+=jump_lookup(temp_jump.group(3))
		else:
			#if there is a jump involved
			if re.search(';',line) is None:
				temp_dest=re.search('(.*)(\=)(.*)',line)
				toWrite+=comp_lookup(temp_dest.group(3))
				toWrite+=dest_lookup(temp_dest.group(1))
				toWrite+=jump_lookup('null')
			else:
				temp_dest = re.search('(.*)(\=)(.*)(;)(.*)',line)
				toWrite+=comp_lookup(temp_dest.group(3))
				toWrite+=dest_lookup(temp_dest.group(1))
				toWrite+=jump_lookup(temp_dest.group(5))
		line_num+=1
	
	if len(toWrite) > 0:
		output+=toWrite+'\n'
		toWrite=''
#End for loop
print(line_num)

IN.close()
output = user_def_replace(output,symbol_table,user_def_count)
output = clean_out(output)
OUT.write(output)
OUT.close()


#---------------------------End Program----------------------------------------