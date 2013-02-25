import sys, string, os, io,re
#------------------------------------------------------------------------------
#Chris Card
#CS410
#ECS project 06
#Due:2/25/13
#------------------------------------------------------------------------------

class Parser:

	#Inputed parameters
	extend_op=False

	#Constance
	a_type='A_COMMAND'
	c_type='C_COMMAND'
	l_type='L_COMMAND'

	#File parsing parameters
	line=''
	line_num=0
	cType=''
	sym=''
	dest_=''
	jump_=''
	comp_=''
	neOf=True



	def __init__(self,filein,extendedop):
		self.infile = open(filein)
		self.extend_op = extendedop

	#--------------------------------------------------------------------------
	# Returns true if it has more commands
	def hasMoreCommands(self):
		return self.neOf

	#--------------------------------------------------------------------------
	# Returns the command type
	def commandType(self):
		return self.cType

	#--------------------------------------------------------------------------
	# returns the symbol
	def symbol(self):
		return self.sym

	#--------------------------------------------------------------------------
	# returns the command
	def comp(self):
		return self.comp_

	#--------------------------------------------------------------------------
	#returns destination
	def dest(self):
		return self.dest_

	#--------------------------------------------------------------------------
	#returns the jump
	def jump(self):
		return self.jump_

	#--------------------------------------------------------------------------
	# Advance parser to next line
	def advance(self):
		#Ensures that if it is invalid symbol or
		#command it will cause an error when trying to look it up
		self.cType='null'
		self.sym='null'
		self.dest_='null'
		self.jump_='null'
		self.comp_='null'

		#checks for EOF
		temp = self.infile.tell()
		self.line = self.infile.readline()
		if temp == self.infile.tell():
			self.infile.close()
			self.neOf=False
			return

		self.line = self.line.strip()

		#a type command
		if re.search('^\@.*',self.line) is not None:
			self.line = self.line.lstrip('@')
			#checks for invalid symbol or label
			if re.search('^[0-9]+[A-Za-z\_\.\$\:]+',self.line) is not None:
				print('invalide label or symbol '+self.line+' at approx line '+
					repr(self.line_num))
				sys.exit(0)

			self.cType=self.a_type
			self.sym = self.line
			self.line_num+=1
	
		#User deffined variable
		elif re.search('^\(.*\)[0-9]+',self.line) is not None and self.extend_op:
			temp_udef = re.search('(^\(.*\))([0-9]+)',self.line)
			self.cType=self.l_type
			self.sym=temp_udef.group(1)+';'+temp_udef.group(2)
			self.line_num+=1
	
		#If label
		elif re.search('^\(.*\)',self.line) is not None:
			self.cType=self.l_type
			self.sym=self.line+';'+repr(self.line_num)
	
		#If line is a command and not empty
		elif re.search('^\/\/',self.line) is None and len(self.line) > 1:
			#If there is a comment at end of line
			if re.search('.*\/\/.*',self.line) is not None:
				#Strips comment off
				temp_line = re.search('(.*)(\/\/.*)',self.line)
				self.line=temp_line.group(1)
				self.line=self.line.strip()

			self.cType=self.c_type
			#If there is a destination involved
			if re.search('\=',self.line) is None:
				#If there is a jump involved
				if re.search(';',self.line) is None:
					self.comp_ = self.line
				else:
					temp_jump = re.search('(.*)(;)(.*)',self.line)
					self.comp_=temp_jump.group(1)
					self.jump_=temp_jump.group(3)
			else:
				#If there is a jump involved
				if re.search(';',self.line) is None:
					temp_dest=re.search('(.*)(\=)(.*)',self.line)
					self.comp_=temp_dest.group(3)
					self.dest_=temp_dest.group(1)
				else:
					temp_dest = re.search('(.*)(\=)(.*)(;)(.*)',self.line)
					self.comp_=temp_dest.group(3)
					self.dest_=temp_dest.group(1)
					self.jump_=temp_dest.group(5)
			self.line_num+=1