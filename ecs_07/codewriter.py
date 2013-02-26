import sys, string, os, io,re
#------------------------------------------------------------------------------
#Chris Card
#CS410
#ECS project 06
#Due:3/4/13
#------------------------------------------------------------------------------

class Parser:


#------------------------------------------------------------------------------
# Cretes push commands
def push(p_val):
	
	return temp_

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

	#------------------------------------------------------------------------------
	# inits the sp pointer
	def init_sp(self):
		temp_s = "@256\n"
		temp_s += "D=A\n\n"
		temp_s += "@sp\n"
		temp_s += "M=D\n\n"
		self.outfile.write(temp_s)


	#--------------------------------------------------------------------------
	#the constructor
	def __init__(self,fileout):
		self.outfile = open(fileout, 'w')

	#--------------------------------------------------------------------------
	#closes the current file
	def Close(self):
		self.outfile.close()

	#--------------------------------------------------------------------------
	#opens new outfile
	def setFileName(self, fileout):
		self.outfile = open(fileout, 'w')

	#--------------------------------------------------------------------------
	# writes arithmatic commands
	def writeArithmetic(self, command):
		if 'add' in command:
			temp_s = "@SP\n"
			temp_s += "M=M-1\n"
			temp_s += "A=M\n"
			temp_s += "D=M\n\n"
			temp_s += "@SP\n"
			temp_s += "M=M-1\n"
			temp_s += "A=M\n"
			temp_s += "M=D+M\n\n"
			temp_s += "@SP\n"
			temp_s += "M=M+1\n\n"
			self.outfile.write(temp_s)
		elif 'sub' in command:
			temp_s = "@SP\n"
			temp_s += "M=M-1\n"
			temp_s += "A=M\n"
			temp_s += "D=M\n\n"
			temp_s += "@R13\n"
			temp_s += "M=D\n\n"
			temp_s += "@SP\n"
			temp_s += "M=M-1\n"
			temp_s += "A=M\n"
			temp_s += "D=M\n\n"
			temp_s += "@R13\n"
			temp_s += "D=D-M\n\n"
			temp_s = "@SP\n"
			temp_s += "A=M\n"
			temp_s += "M=D\n\n"
			temp_s += "@SP\n"
			temp_s += "M=M+1\n\n"
			self.outfile.write(temp_s)
		elif 'neg' in command:
			temp_s = "@SP\n"
			temp_s += "M=M-1\n"
			temp_s += "A=M\n"
			temp_s += "D=M\n\n"
			temp_s += "@1\n"
			temp_s += "D=-D\n"
			temp_s = "@SP\n"
			temp_s += "A=M\n"
			temp_s += "M=D\n\n"
			temp_s += "@SP\n"
			temp_s += "M=M+1\n\n"
			self.outfile.write(temp_s)
		elif 'eq' in command:
			pass
		elif 'lt' in command:
			pass
		elif 'gt' in command:
			pass
		elif 'and' in command:
			temp_s = "@SP\n"
			temp_s += "M=M-1\n"
			temp_s += "A=M\n"
			temp_s += "D=M\n\n"
			temp_s += "@SP\n"
			temp_s += "M=M-1\n"
			temp_s += "A=M\n"
			temp_s += "M=D&M\n\n"
			temp_s += "@SP\n"
			temp_s += "M=M+1\n\n"
			self.outfile.write(temp_s)
		elif 'or' in command:
			temp_s = "@SP\n"
			temp_s += "M=M-1\n"
			temp_s += "A=M\n"
			temp_s += "D=M\n\n"
			temp_s += "@SP\n"
			temp_s += "M=M-1\n"
			temp_s += "A=M\n"
			temp_s += "M=D|M\n\n"
			temp_s += "@SP\n"
			temp_s += "M=M+1\n\n"
			self.outfile.write(temp_s)
		elif 'not' in command:
			temp_s = "@SP\n"
			temp_s += "M=M-1\n"
			temp_s += "A=M\n"
			temp_s += "D=M\n"
			temp_s += "M=!D\n\n"
			temp_s += "@SP\n"
			temp_s += "M=M+1\n\n"
			self.outfile.write(temp_s)

	#--------------------------------------------------------------------------
	#writes appropriate push pop commands
	def writePushPop(self, cType, segment, index):
		if push_type in cType:
			if 'constant' in segment:
				temp_s = "@"+index+"\n"
				temp_s += "D=A\n\n"
				temp_s += "@SP\n"
				temp_s += "A=M\n"
				temp_s += "M=D\n\n"
				temp_s += "@SP\n"
				temp_s += "M=M+1\n\n"
				self.outfile.write(temp_s)
			else:
				temp_s = "@"+index+"\n"
				temp_s += "D=A\n\n"
				temp_s += "@"+segment+"\n"
				temp_s += "A=D+M\n"
				temp_s += "D=M\n\n"
				temp_s += "@SP\n"
				temp_s += "A=M\n"
				temp_s += "M=D\n\n"
				temp_s += "@SP\n"
				temp_s += "M=M+1\n\n"
				self.outfile.write(temp_s)
		else:
			if 'constant' in segment:
				temp_s = "@SP\n"
				temp_s += "M=M-1\n\n"
				self.outfile.write(temp_s)
			else:
				temp_s = "@"+index+"\n"
				temp_s += "D=A\n\n"
				temp_s += "@"+segment+"\n"
				temp_s += "A=D+M\n"
				temp_s += "D=A\n\n"
				temp_s += "@R13\n"
				temp_s += "M=D\n\n"
				temp_s += "@SP\n"
				temp_s += "M=M-1\n"
				temp_s += "A=M\n"
				temp_s += "D=M\n\n"
				temp_s += "@R13\n"
				temp_s += "A=M\n"
				temp_s += "M=D\n\n"
				self.outfile.write(temp_s)
