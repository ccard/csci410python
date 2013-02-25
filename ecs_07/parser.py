import sys, string, os, io,re
#------------------------------------------------------------------------------
#Chris Card
#CS410
#ECS project 06
#Due:3/4/13
#------------------------------------------------------------------------------

class Parser:

	#Inputed parameters
	extend_op=False

	#Constance
	arith_type='C_ARITHMETIC'
	push_type='C_PUSH'
	pop_type='C_POP'
	lable_type='C_LABEL'
	goto_type='C_GOTO'
	if_type='C_IF'
	funct_type='C_FUNCTION'
	ret_type='C_RETURN'
	call_type='C_CALL'

	#File parsing parameters
	line=''
	line_num=0
	cType=''
	arg1=''
	arg2=''
	
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
	def arg_1(self):
		return self.arg1

	#--------------------------------------------------------------------------
	# returns the command
	def arg_2(self):
		return self.arg2

	#--------------------------------------------------------------------------
	# Advance parser to next line
	def advance(self):
		#Ensures that if it is invalid symbol or
		#command it will cause an error when trying to look it up
		self.cType='null'
		self.arg1='null'
		self.arg2='null'

		#checks for EOF
		temp = self.infile.tell()
		self.line = self.infile.readline()
		if temp == self.infile.tell():
			self.infile.close()
			self.neOf=False
			return

		self.line = self.line.strip()

		if re.search('^function .*', self.line) is not None:
			cType = funct_type
			temp_f = re.split('\S+',self.line)
			first=False
			second=False
			for p in temp_f:
				if first:
					arg1 = p
					first=False
					second=True
				elif second:
					arg2 = p
					second=False
				else:
					first=True

		elif re.search('^label .*',self.line) is not None:
			cType = lable_type
			temp_l = re.search('(^label\S+)(.*)',self.line)
			arg1 = temp_l.group(2)
		elif re.search('^return',self.line) is not None:
			cType = ret_type;
		elif re.search('^pop .*',self.line) is not None:
			cType = pop_type

			temp_po = re.split('\S+',self.line)
			first=False
			second=False
			for p in temp_po:
				if first:
					arg1 = p
					first=False
					second=True
				elif second:
					arg2 = p
					second=False
				else:
					first=True

		elif re.search('^push .*',self.line) is not None:
			cType = push_type

			temp_pu = re.split('\S+',self.line)
			first=False
			second=False
			for p in temp_pu:
				if first:
					arg1 = p
					first=False
					second=True
				elif second:
					arg2 = p
					second=False
				else:
					first=True

		elif re.search('^if-goto .*',self.line) is not None:
			cType = if_type+' '+goto_type
			#not used in this project
		self.line_num+=1