import sys, string, os, io,re
from jacktokenizer import JackToken
#from compilationengine import CompilationEngine
#------------------------------------------------------------------------------
#Chris Card
#CS410
#ECS project 10
#python 3.3
#Due:3/25/13
#This tokenizes the jack file
#------------------------------------------------------------------------------


#------------------------------------------------------------------------------
# Var Dec:
#------------------------------------------------------------------------------

in_file = ''
out_file = ''
offset = 2
space = ' '

#------------------------------------------------------------------------------
# Check user in:
#------------------------------------------------------------------------------
if len(sys.argv) < 2: #Checks to see if user put in file
	print('incorrect number of args!')	
	print('assembler.py <file.vm|directry path>')
	sys.exit(0)

in_file=sys.argv[1]

#Strips .vm of the end and adds .asm
temp_out=re.search('(.*)(\.jack)',in_file)
out_file+=temp_out.group(1)+'T2.xml'

#------------------------------------------------------------------------------
# Main:
#------------------------------------------------------------------------------
token = JackToken(in_file)
out = open(out_file,'w')
out.write("<tokens>\n")
while token.hasMoreTokens():
	token.advance()
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
	elif 'STRING_CONST' in tokenType():
		out.write((space*offset)+"<stringConstant>"+token.stringVal()+"</stringConstant>\n")

out.write("</tokens>")
out.close()




#------------------------End Main----------------------------------------------