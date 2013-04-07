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
#   JackCompiler.py <option(optional)> <path to directory|filename>
#			<option> = -t for tokenizer
#					   omit for full compiler
#			<path to directory|filename> = is the path to the directory 
#								containing files to compile or the file to
#								compile
#Output:
#	The output file(s) are stored in the same directory as the input file(s)
#	except the output file(s) are in the following formate '*2.xml' so as
#	to not interfier with the installed files 
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
	print('Incorrect number of args!')	
	print('JackCompiler.py <option(optional)> <path to directory|filename>')
	sys.exit(0)

#if option was chosen to generate the tokenized output
if len(sys.argv) == 3:
	in_file=sys.argv[2]
	fullCompiler = False

	#Checks for correct file name if not then assumes directory
	if re.search('.*\.jack',in_file) is None:
		is_dir=True

		#goes through the directory and finds the .jack files
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

#If choose to run full compiler
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

if fullCompiler: #if option was ommited meaning full compilation
	if is_dir: #if it is a directory compile all '*.jack' files
		for d in directory:
			#strips '.jack' off the end and adds '2.xml'
			temp_out = re.search('(.*)(\.jack)',d)
			out_file = temp_out.group(1)+'2.xml'

			compiler = CompilationEngine(d,out_file)
			compiler.compileClass()

	else: #if not a directory
		compiler = CompilationEngine(in_file,out_file)
		compiler.compileClass()

else: #option for tokenized output selected
	if is_dir: #if it is a directory
		for d in directory:
			#Strips '.jack' off the end and adds 'T2.xml'
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

	else: #just a file
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