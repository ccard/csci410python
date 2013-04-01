import sys, string, os, io,re
from jacktokenizer import JackToken
from compilationengine import CompilationEngine
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

infile = ''

#------------------------------------------------------------------------------
# Check user in:
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
# Main:
#------------------------------------------------------------------------------





#------------------------End Main----------------------------------------------