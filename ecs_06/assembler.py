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
def symbol_lookup(sym,line_num,is_label,user_def,symbol_table):
	sym=sym.strip('()')
	if sym in symbol_table:
		if is_label:
			bi = bin(line_num)
			bi = bi.lstrip('-0b')
			dif = 16 - len(bi)
			bi = '0'*dif+bi
			old=symbol_table[sym]
			symbol_table[sym]=bi
			return 's'+'('+sym+')'+bi+';'+'('+sym+')'+old

		else:
			return symbol_table[sym]

	else:
		if is_label:
			bi = bin(line_num)
			bi = bi.lstrip('-0b')
			dif = 16 - len(bi)
			bi = '0'*dif+bi
			symbol_table[sym]=bi
			return '('+sym+')'+bi

		elif re.search('[A-Za-z\_\.\$\:]+[0-9]*[A-Za-z\_\.\$\:]*',sym) is not None:
			bi = bin(user_def)
			bi = bi.lstrip('-0b')
			dif = 16 - len(bi)
			bi = '0'*dif+bi
			symbol_table[sym]=bi
			return 'uc'+'('+sym+')'+bi

		else:
			bi = bin(int(sym))
			bi = bi.lstrip('-0b')
			dif = 16 - len(bi)
			bi = '0'*dif+bi
			symbol_table[sym]=bi
			return '('+sym+')'+bi

#------------------------------------------------------------------------------
#This goes back an replaces the appropriate value in the input
def search_replace(original,newline):
	newline = newline.lstrip('s')
	old_new = re.split(';',newline)
	old=old_new[1]
	old=old.strip('\n')
	new=old_new[0]
	
	listOrig = re.split('\n+',original)

	newOld=''

	for line in listOrig:

		if old in line:
			newOld+=new+'\n'

		elif len(line)>0:
			newOld+=line+'\n'
			
	
	return newOld

#------------------------------------------------------------------------------
#cleans the output of (sym)
def clean_out(to_clean):
	listOrig = re.split('\n+',to_clean)

	newOld=''

	for line in listOrig:
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
if len(sys.argv) < 2:
	print('incorrect number of args!')
	print('assembler.py <file.asm>')
	sys.exit(0)

in_file=sys.argv[1]

if re.search('.*\.asm',in_file) == None:
	print('incorrect file name!')
	sys.exit(0)

out_file=in_file.strip('.asm')
out_file+='.hack'

#------------------------------------------------------------------------------
#Main
#------------------------------------------------------------------------------
IN=open(in_file)
OUT=open(out_file,'w')

toWrite=''
output=''
line_num=0
for line in IN:
	line = line.strip()

	if re.search('^\@.*',line) is not None:
		line = line.lstrip('@')
		toWrite+=symbol_lookup(line,line_num,False,user_def_count,symbol_table)
		if re.search('uc',toWrite) is not None:
			temp = re.search('(uc)(.*)',toWrite)
			toWrite = temp.group(2)
			user_def_count+=1
		
		line_num+=1

	elif re.search('^\(.*\)',line) is not None:
		temp_s = symbol_lookup(line,line_num,True,user_def_count,symbol_table)
		
		if re.search('s.*\;.*',temp_s) is not None:
			output = search_replace(output,temp_s)
			
		if re.search('uc',temp_s) is not None:
			user_def_count+=1

	elif re.search('^\/\/',line) is None and len(line) > 1:
		toWrite='111'
		
		if re.search('.*\/\/.*',line) is not None:
			temp_line = re.search('(.*)(\/\/.*)',line)
			line=temp_line.group(1)
			line=line.strip()

		if re.search('=.*M.*',line) is None:
			toWrite+='0'
		else:
			toWrite+='1'

		if re.search('\=',line) is None:
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
output = clean_out(output)
OUT.write(output)
OUT.close()


#---------------------------End Program----------------------------------------