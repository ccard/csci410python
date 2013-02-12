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
#looks up symbol if it isn't there adds it
def symbol_lookup(sym,line_num,is_label):
	temp_sym=sym.strip('(')
	temp_sym=sym.strip(')')
	if temp_sym in symbol_table:
		if is_label:
			sym = sym.strip('(')
			sym = sym.strip(')')
			bi = bin(line_num)
			bi = bi.strip('-0b')
			dif = 15 - len(bi)
			bi = '0'*dif+bi
			old=symbol_table[sym]
			symbol_table[sym]=bi
			return 's'+bi+';'+old
		else:
			return symbol_table[temp_sym]
	else:
		if is_label:
			sym = sym.strip('(')
			sym = sym.strip(')')
			bi = bin(line_num)
			bi = bi.strip('-0b')
			dif = 15 - len(bi)
			bi = '0'*dif+bi
			symbol_table[sym]=bi
			return bi
		else:
			bi = bin(user_def_count)
			bi = bi.strip('-0b')
			dif = 15 - len(bi)
			bi = '0'*dif+bi
			symbol_table[sym]=bi
			user_def_count +=1
			return bi

#------------------------------------------------------------------------------
#This goes back an replaces the appropriate value in the input
def search_replace(original,newline):
	newline = newline.strip('s')
	old_new = re.split(';',newline)
	old=old_new[1]
	newline=old_new[0]

	listOrig = re.split('\n',original)
	newOld=''
	for line in listOrig:
		if line == old:
			newOld+=newline+'\n'
		else:
			newOld+=line+'\n'

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

symbol_table={'SP':'0','LCL':'1','ARG':'2','THIS':'3','THAT':'4',
			 'R0':'0','R1':'1','R2':'2','R3':'3','R4':'4','R5':'5','R6':'6',
			 'R7':'7','R8':'8','R9':'9','R10':'10','R11':'11','R12':'12',
			 'R13':'13','R14':'14','R15':'15','SCREEN':'16384','KBD':'24576'}

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

temp_out=re.search('(.*)(\.asm)',in_file)
out_file=temp_out.group(0)
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
	if re.search('^\@.*',line) != None:
		toWrite+='0'
		line = line.strip('@')
		toWrite+=symbol_lookup(line,line_num,False)
		line_num+=1

	elif re.search('^\(.*\)',line) != None:
		temp_s = symbol_lookup(line,line_num,True)
		if re.search('s.*\;.*',temp_s) != None:
			output = search_replace(output,temp_s)
		line_num+=1

	elif re.search('^\/\/',line) == None:
		toWrite='111'

		if re.search('.*\/\/.*',line) != None:
			temp_line = re.search('(.*)(\/\/.*)')
			line=temp_line.group(0)

		if re.search('M',line) == None:
			toWrite+='0'
		else:
			toWrite+='1'

		if re.search('\=',line) == None:
			if re.search(';',line) == None:
				toWrite+=comp_lookup(line)
				toWrite+=dest_lookup('null')
				toWrite+=jump_lookup('null')
			else:
				temp_jump = re.search('(.*)(;)(.*)')
				toWrite+=comp_lookup(temp_jump.group(0))
				toWrite+=dest_lookup('null')
				toWrite+=jump_lookup(temp_jump.group(2))
		else:
			if re.search(';',line) == None:
				temp_dest=re.search('(.*)(\=)(.*)')
				toWrite+=comp_lookup(temp_dest.group(2))
				toWrite+=dest_lookup(temp_dest.group(0))
				toWrite+=jump_lookup('null')
			else:
				temp_dest = re.search('(.*)(\=)(.*)(;)(.*)')
				toWrite+=comp_lookup(temp_dest.group(2))
				toWrite+=dest_lookup(temp_dest.group(0))
				toWrite+=jump_lookup(temp_dest.group(4))
		line_num+=1
	
	if len(toWrite) > 0:
		output+=toWrite+'\n'
		toWrite=''
#End for loop

IN.close()

OUT.write(output)
OUT.close()


#---------------------------End Program----------------------------------------