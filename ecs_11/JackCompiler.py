import sys, string, os, io,re
from compilationengine import CompilationEngine
from compilationenginexml import CompilationEngineXML
#------------------------------------------------------------------------------
#Chris Card
#CS410
#ECS project 10
#python 3.3
#Due:4/22/13
#This tokenizes and compiles the jack file Main Program
#Use:
#   JackCompiler.py <option(optional)> <path to directory|filename>
#			<option> = -x for xml
#					   omit for full compiler
#			<path to directory|filename> = is the path to the directory 
#								containing files to compile or the file to
#								compile
#Output:
#	The output file(s) are stored in the same directory as the input file(s)
#	except the output file(s) are in the following formate '*.vm'
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
	option = sys.argv[1]
	fullCompiler = False

	if '-x' in option:
		#Checks for correct file name if not then assumes directory
		if re.search('.*\.jack',in_file) is None:
			is_dir=True
	
			#goes through the directory and finds the .jack files
			temp = os.listdir(in_file)
			for f in temp:
				if re.search('.*\.jack$',f) is not None:
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

	else:
		print('Incorrect option')
		print('JackCompiler.py <option(optional)> <path to directory|filename>')
		sys.exit(0)

#If choose to run full compiler
else:
	in_file=sys.argv[1]

	#Checks for correct file name if not then assumes directory
	if re.search('.*\.jack',in_file) is None:
		is_dir=True

		#goes through the directory and finds the .vm files
		temp = os.listdir(in_file)
		for f in temp:
			if re.search('.*\.jack$',f) is not None:
				temp_s = in_file+"/"+f
				directory.append(temp_s)
		
		#if no files found in directory then error
		if len(directory) == 0:
			print("Error no '*.jack' files in path "+in_file)
			sys.exit(0)

	else:
		#Strips .jack off the end and adds .xml
		temp_out=re.search('(.*)(\.jack)',in_file)
		out_file+=temp_out.group(1)+'.vm'



#------------------------------------------------------------------------------
# Main:
#------------------------------------------------------------------------------

if fullCompiler: #if option was ommited meaning full compilation
	if is_dir: #if it is a directory compile all '*.jack' files
		for d in directory:
			#strips '.jack' off the end and adds '.vm'
			temp_out = re.search('(.*)(\.jack)',d)
			out_file = temp_out.group(1)+'.vm'

			#prints out what file it is compiling at the moment
			print("Compiling: "+d+"....")

			compiler = CompilationEngine(d,out_file)
			compiler.compileClass()

	else: #if not a directory
		compiler = CompilationEngine(in_file,out_file)
		compiler.compileClass()

else: #option for tokenized output selected
	if is_dir: #if it is a directory
		for d in directory:
			#Strips '.jack' off the end and adds '2.xml'
			temp_out = re.search('(.*)(\.jack)',d)
			out_file = temp_out.group(1)+'2.xml'

			compilerxml = CompilationEngineXML(d,out_file)
			compilerxml.compileClass()

	else: #just a file
		compilerxml = CompilationEngineXML(in_file,out_file)
		compilerxml.compileClass()



#------------------------End Main----------------------------------------------