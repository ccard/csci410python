import sys, string, os, io,re
#------------------------------------------------------------------------------
#Chris Card
#CS410
#ECS project 07
#python 3.3
#Due:3/4/13
#------------------------------------------------------------------------------

class Parser:


	#Constance
	arith_type='C_ARITHMETIC'
	push_type='C_PUSH'
	pop_type='C_POP'
	lable_type='C_LABEL'
	goto_type='C_GOTO'
	if_type='C_IF-C_GOTO'
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


	def __init__(self,filein):
		self.infile = open(filein)

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
		#sets args to empty string and cType to null
		self.cType='null'
		self.arg1=''
		self.arg2=''

		#checks for EOF
		temp = self.infile.tell()
		self.line = self.infile.readline()
		if temp == self.infile.tell():
			self.infile.close()
			self.neOf=False
			return

		self.line = self.line.strip()

		if re.search('^add', self.line) is not None:
			self.cType = self.arith_type
			self.arg1 = self.line

		elif re.search('^sub', self.line) is not None:
			self.cType = self.arith_type
			self.arg1 = self.line

		elif re.search('^neg', self.line) is not None:
			self.cType = self.arith_type
			self.arg1 = self.line

		elif re.search('^lt', self.line) is not None:
			self.cType = self.arith_type
			self.arg1 = self.line

		elif re.search('^eq', self.line) is not None:
			self.cType = self.arith_type
			self.arg1 = self.line

		elif re.search('^gt', self.line) is not None:
			self.cType = self.arith_type
			self.arg1 = self.line

		elif re.search('^and', self.line) is not None:
			self.cType = self.arith_type
			self.arg1 = self.line

		elif re.search('^or', self.line) is not None:
			self.cType = self.arith_type
			self.arg1 = self.line
			
		elif re.search('^not', self.line) is not None:
			self.cType = self.arith_type
			self.arg1 = self.line

		elif re.search('^function .*', self.line) is not None:
			self.cType = self.funct_type
			temp_f = re.split('\s+',self.line)
			first=False
			second=False
			count = 0
			for p in temp_f:
				if count >= 2:
					break
				elif first:
					count += 1
					self.arg1 = p
					first=False
					second=True
				elif second:
					count += 1
					self.arg2 = p
					second=False
				else:
					first=True

		elif re.search('^call .*',self.line) is not None:
			self.cType = self.call_type
			#reviesed regex that gets that ensures that any comments at the EOL
			#aren't included in the function name
			temp_c = re.search('(^call\s+)([A-Za-z0-9\.\_\:\$]+)(\s+)([0-9]+)(.*)',self.line)
			self.arg1 = temp_c.group(2)
			self.arg2 = temp_c.group(4)

		elif re.search('^label .*',self.line) is not None:
			self.cType = self.lable_type
			#This ensures any comments at EOL aren't captured as part of the
			#label
			temp_l = re.search('(^label\s+)([A-Za-z0-9\_\.\:\$]*)([\s\/.]*)',self.line)
			self.arg1 = temp_l.group(2)

		elif re.search('^return',self.line) is not None:
			self.cType = self.ret_type;

		elif re.search('^pop .*',self.line) is not None:
			self.cType = self.pop_type

			temp_po = re.split('\s+',self.line)
			first=False
			second=False
			count = 0
			for p in temp_po:
				if count >= 2:
					break
				elif first:
					count += 1
					self.arg1 = p
					first=False
					second=True
				elif second:
					count += 1
					self.arg2 = p
					second=False
				else:
					first=True

		elif re.search('^push .*',self.line) is not None:
			self.cType = self.push_type

			temp_pu = re.split('\s+',self.line)
			first=False
			second=False
			count = 0
			for p in temp_pu:
				if count >= 2:
					break
				elif first:
					count += 1
					self.arg1 = p
					first=False
					second=True
				elif second:
					count += 1
					self.arg2 = p
					second=False
				else:
					first=True

		elif re.search('^if-goto .*',self.line) is not None:
			self.cType = self.if_type
			temp_ifg = re.search('(^if-goto\s+)(.*)',self.line)
			self.arg1 = temp_ifg.group(2)

		elif re.search('^goto .*',self.line) is not	None:
			self.cType = self.goto_type
			temp_gt = re.search('(^goto\s+)(.*)',self.line)
			self.arg1 = temp_gt.group(2)
		
		self.line_num+=1