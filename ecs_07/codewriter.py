import sys, string, os, io,re
#------------------------------------------------------------------------------
#Chris Card
#CS410
#ECS project 06
#Due:3/4/13
#------------------------------------------------------------------------------

class CodeWriter:

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

	#jump counters
	eq_jump=0
	lt_jump=0
	gt_jump=0


	#--------------------------------------------------------------------------
	#the constructor
	def __init__(self):
		pass

	#--------------------------------------------------------------------------
	# inits the sp pointer
	def init_sp(self):
		temp_s = "//This initializes the stack pointer\n"
		temp_s += "@256\n"
		temp_s += "D=A\n\n"
		temp_s += "@sp\n"
		temp_s += "M=D\n\n"
		self.outfile.write(temp_s)

	#--------------------------------------------------------------------------
	#closes the current file
	def Close(self):
		self.outfile.close()

	#--------------------------------------------------------------------------
	#opens new outfile
	def setFileName(self, fileout):
		self.outfile = open(fileout, 'w')
		#self.init_sp()

	#--------------------------------------------------------------------------
	# writes arithmatic commands
	def writeArithmetic(self, command):
		if 'add' in command:
			temp_s = "//This is the add command\n"
			temp_s += "@SP\n"
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
			temp_s = "//This is the sub command\n"
			temp_s += "@SP\n"
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
			temp_s += "@SP\n"
			temp_s += "AM=M+1\n"
			temp_s += "A=A-1\n"
			temp_s += "M=D\n\n"
			self.outfile.write(temp_s)
		elif 'neg' in command:
			temp_s = "//This is the neg command\n"
			temp_s += "@SP\n"
			temp_s += "M=M-1\n"
			temp_s += "A=M\n"
			temp_s += "D=M\n\n"
			temp_s += "@1\n"
			temp_s += "D=-D\n"
			temp_s += "@SP\n"
			temp_s += "AM=M+1\n"
			temp_s += "A=A-1\n"
			temp_s += "M=D\n\n"
			self.outfile.write(temp_s)
		elif 'eq' in command:
			temp_s = "//This is the eq logical\n"
			temp_s += "@SP\n"
			temp_s += "M=M-1\n"
			temp_s += "A=M\n"
			temp_s += "D=M\n\n"
			temp_s += "@SP\n"
			temp_s += "M=M-1\n"
			temp_s += "A=M\n"
			temp_s += "D=D-M\n\n"
			temp_s += "@eq."+repr(self.eq_jump)+"\n"
			temp_s += "D;JEQ\n\n"
			temp_s += "@R13\n"
			temp_s += "D=-1\n\n"
			temp_s += "(eq."+repr(self.eq_jump)+")\n\n"
			temp_s += "@SP\n"
			temp_s += "AM=M+1\n"
			temp_s += "A=A-1\n"
			temp_s += "M=!D\n\n"
			self.eq_jump += 1
			self.outfile.write(temp_s)
		elif 'lt' in command:
			temp_s = "//This is the lt logical\n"
			temp_s += "@SP\n"
			temp_s += "M=M-1\n"
			temp_s += "A=M\n"
			temp_s += "D=M\n\n"
			temp_s += "@SP\n"
			temp_s += "M=M-1\n"
			temp_s += "A=M\n"
			temp_s += "D=D-M\n\n"
			temp_s += "@lt.false."+repr(self.lt_jump)+"\n"
			temp_s += "D;JLE\n\n"
			temp_s += "@R13\n"
			temp_s += "D=-1\n\n"
			temp_s += "@lt."+repr(self.lt_jump)+"\n"
			temp_s += "0;JMP\n\n"
			temp_s += "(lt.false."+repr(self.lt_jump)+")\n\n"
			temp_s += "@0\n"
			temp_s += "D=A\n\n"
			temp_s += "(lt."+repr(self.lt_jump)+")\n\n"
			temp_s += "@SP\n"
			temp_s += "AM=M+1\n"
			temp_s += "A=A-1\n"
			temp_s += "M=D\n\n"
			self.lt_jump += 1
			self.outfile.write(temp_s)
		elif 'gt' in command:
			temp_s = "//This is the gt logical\n"
			temp_s += "@SP\n"
			temp_s += "M=M-1\n"
			temp_s += "A=M\n"
			temp_s += "D=M\n\n"
			temp_s += "@SP\n"
			temp_s += "M=M-1\n"
			temp_s += "A=M\n"
			temp_s += "D=D-M\n\n"
			temp_s += "@gt.false."+repr(self.gt_jump)+"\n"
			temp_s += "D;JGE\n\n"
			temp_s += "@R13\n"
			temp_s += "D=-1\n\n"
			temp_s += "@gt."+repr(self.gt_jump)+"\n"
			temp_s += "0;JMP\n\n"
			temp_s += "(gt.false."+repr(self.gt_jump)+")\n\n"
			temp_s += "@0\n"
			temp_s += "D=A\n\n"
			temp_s += "(gt."+repr(self.gt_jump)+")\n\n"
			temp_s += "@SP\n"
			temp_s += "AM=M+1\n"
			temp_s += "A=A-1\n"
			temp_s += "M=D\n\n"
			self.gt_jump += 1
			self.outfile.write(temp_s)
		elif 'and' in command:
			temp_s = "//This is the and logical\n"
			temp_s += "@SP\n"
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
			temp_s = "//This is the or logical\n"
			temp_s += "@SP\n"
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
			temp_s = "//This is the not logical\n"
			temp_s += "@SP\n"
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
		if self.push_type in cType:
			temp_s = "//This is the push command\n"
			if 'constant' in segment:
				temp_s += "@"+index+"\n"
				temp_s += "D=A\n\n"
				temp_s += "@SP\n"
				temp_s += "AM=M+1\n"
				temp_s += "A=A-1\n"
				temp_s += "M=D\n\n"
				self.outfile.write(temp_s)
			else:
				temp_s += "@"+index+"\n"
				temp_s += "D=A\n\n"
				temp_s += "@"+segment+"\n"
				temp_s += "A=D+M\n"
				temp_s += "D=M\n\n"
				temp_s += "@SP\n"
				temp_s += "AM=M+1\n"
				temp_s += "A=A-1\n"
				temp_s += "M=D\n\n"
				self.outfile.write(temp_s)
		else:
			temp_s = "//This is the pop command\n"
			if 'constant' in segment:
				temp_s += "@SP\n"
				temp_s += "M=M-1\n\n"
				self.outfile.write(temp_s)
			else:
				temp_s += "@"+index+"\n"
				temp_s += "D=A\n\n"
				temp_s += "@"+segment+"\n"
				temp_s += "D=D+M\n"
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
