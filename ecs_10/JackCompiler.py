import sys, string, os, io,re
from jacktokenizer import JackToken
from compilationengine import CompilationEngine
#------------------------------------------------------------------------------
#Chris Card
#CS410
#ECS project 10
#python 3.3
#Due:3/25/13
#This tokenizes and compiles the jack file Main Program
#Use:
#   JackCompiler.py <option(optional)> <location(optional)/filename>
#			<option> = -t for tokenizer
#					   omit for full compiler
#------------------------------------------------------------------------------


#------------------------------------------------------------------------------
# Var Dec:
#------------------------------------------------------------------------------

in_file = ''
out_file = ''
offset = 2
space = ' '
directory = []
fullCompiler = True
is_dir = False

#------------------------------------------------------------------------------
# Check user in:
#------------------------------------------------------------------------------
if len(sys.argv) < 2: #Checks to see if user put in file
	print('incorrect number of args!')	
	print('JackCompiler.py <option(optional)> <file.vm|directry path>')
	sys.exit(0)

if len(sys.argv) == 3:
	in_file=sys.argv[2]
	fullCompiler = False
	#Checks for correct file name if not then assumes directory
	if re.search('.*\.jack',in_file) is None:
		is_dir=True
		#goes through the directory and finds the .vm files
		temp = os.listdir(in_file)
		for f in temp:
			if re.search('.*\.jack',f) is not None:
				temp_s = in_file+"/"+f
				directory.append(temp_s)
		
		#if no files found in directory then error
		if len(directory) == 0:
			print("Error no '*.jack' files in path "+in_file)
			sys.exit(0)
	else:
		#Strips .jack off the end and adds .xml
		temp_out=re.search('(.*)(\.jack)',in_file)
		out_file+=temp_out.group(1)+'T2.xml'
else:
	in_file=sys.argv[1]
	#Checks for correct file name if not then assumes directory
	if re.search('.*\.jack',in_file) is None:
		is_dir=True
		#goes through the directory and finds the .vm files
		temp = os.listdir(in_file)
		for f in temp:
			if re.search('.*\.jack',f) is not None:
				temp_s = in_file+"/"+f
				directory.append(temp_s)
		
		#if no files found in directory then error
		if len(directory) == 0:
			print("Error no '*.jack' files in path "+in_file)
			sys.exit(0)
	else:
		#Strips .jack off the end and adds .xml
		temp_out=re.search('(.*)(\.jack)',in_file)
		out_file+=temp_out.group(1)+'2.xml'



#------------------------------------------------------------------------------
# Main:
#------------------------------------------------------------------------------
if fullCompiler:
	if is_dir:
		for d in directory:
			temp_out = re.search('(.*)(\.jack)',d)
			out_file = temp_out.group(1)+'2.xml'
			compiler = CompilationEngine(d,out_file)
			compiler.compileClass()
	else:
		compiler = CompilationEngine(in_file,out_file)
		compiler.compileClass()

else:
	if is_dir:
		for d in directory:
			#Strips .jack off the end and adds .xml
			temp_out = re.search('(.*)(\.jack)',d)
			out_file = temp_out.group(1)+'T2.xml'

			token = JackToken(d)
			out = open(out_file,'w')
			out.write("<tokens>\n")
			token.advance()
			while token.hasMoreTokens():
				if 'KEYWORD' in token.tokenType():
					out.write((space*offset)+"<keyword>"+token.keyWord().lower()+"</keyword>\n")
				elif 'SYMBOL' in token.tokenType():
					tempsym = token.symbol()
					if '<' in tempsym:
						tempsym = '&lt;'
					elif '>' in tempsym:
						tempsym = '&gt;'
					elif '&' in tempsym:
						tempsym = '&amp;'
					out.write((space*offset)+"<symbol>"+tempsym+"</symbol>\n")
				elif 'IDENTIFIER' in token.tokenType():
					out.write((space*offset)+"<identifier>"+token.identifier()+"</identifier>\n")
				elif 'INT_CONST' in token.tokenType():
					out.write((space*offset)+"<integerConstant>"+token.intVal()+"</integerConstant>\n")
				elif 'STRING_CONST' in token.tokenType():
					out.write((space*offset)+"<stringConstant>"+token.stringVal()+"</stringConstant>\n")
				token.advance()
		
			out.write("</tokens>")
			out.close()

	else:
		token = JackToken(in_file)
		out = open(out_file,'w')
		out.write("<tokens>\n")
		token.advance()
		while token.hasMoreTokens():
			if 'KEYWORD' in token.tokenType():
				out.write((space*offset)+"<keyword>"+token.keyWord().lower()+"</keyword>\n")
			elif 'SYMBOL' in token.tokenType():
				tempsym = token.symbol()
				if '<' in tempsym:
					tempsym = '&lt;'
				elif '>' in tempsym:
					tempsym = '&gt;'
				elif '&' in tempsym:
					tempsym = '&amp;'
				out.write((space*offset)+"<symbol>"+tempsym+"</symbol>\n")
			elif 'IDENTIFIER' in token.tokenType():
				out.write((space*offset)+"<identifier>"+token.identifier()+"</identifier>\n")
			elif 'INT_CONST' in token.tokenType():
				out.write((space*offset)+"<integerConstant>"+token.intVal()+"</integerConstant>\n")
			elif 'STRING_CONST' in token.tokenType():
				out.write((space*offset)+"<stringConstant>"+token.stringVal()+"</stringConstant>\n")
			token.advance()
	
		out.write("</tokens>")
		out.close()



#------------------------End Main----------------------------------------------