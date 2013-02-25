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
	temp_s += "@"+p_val+"\n"
	temp_s += "D=A\n\n"
	temp_s = "@SP\n"
	temp_s += "A=M\n"
	temp_s += "M=D\n\n"
	temp_s += "@SP\n"
	temp_s += "M=M+1"
	return temp_

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
			temp_s += "M=M-1"
			temp_s += "A=M\n"
			temp_s += "D=M\n\n"
			temp_s += "@SP\n"
			temp_s += "M=M-1"
			temp_s += "A=M\n"
			temp_s += "M=D+M\n\n"
			temp_s += "@SP\n"
			temp_s += "M=M+1"
		elif 'sub' in command:
			temp_s = "@SP\n"
			temp_s += "M=M-1"
			temp_s += "A=M\n"
			temp_s += "D=M\n\n"
			temp_s += "@R5\n"
			temp_s += "M=D\n"
			temp_s += "@SP\n"
			temp_s += "M=M-1"
			temp_s += "A=M\n"
			temp_s += "D=M\n\n"
			temp_s += "@R5\n"
			temp_s += "D=D+M\n\n"
			temp_s = "@SP\n"
			temp_s += "A=M\n"
			temp_s += "M=D\n\n"
			temp_s += "@SP\n"
			temp_s += "M=M+1"


