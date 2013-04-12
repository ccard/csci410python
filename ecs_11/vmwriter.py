import sys, string, os, io,re
#------------------------------------------------------------------------------
#Chris Card
#CS410
#ECS project 10
#python 3.3
#Due:3/25/13
#This writes the vm code to the file
#------------------------------------------------------------------------------

class VMWriter:


	#--------------------------------------------------------------------------
	# Var Dec:
	#--------------------------------------------------------------------------
	arith = {'+':'add','-':'sub','<':'lt','>':'gt','=':'eq','&':'and','|':'or'
			,'~':'not'}
	

	#--------------------------------------------------------------------------
	# Class Dec:
	#--------------------------------------------------------------------------
	
	#--------------------------------------------------------------------------
	# Constructor takes file to write to
	def __init__(self,outfile):
		self.out = open(outfile, 'w')

	#--------------------------------------------------------------------------
	# This writes a push vm comand
	def writePush(self,seg,index):
		self.out.write('push '+seg+' '+index+'\n')

	#--------------------------------------------------------------------------
	# This writes pop vm code
	def writePop(self,seg,index):
		self.out.write('pop '+seg+' '+index+'\n')

	#--------------------------------------------------------------------------
	# This writes arithmetic operation vm code
	def writeArithmetic(self,command):
		if command in self.arith:
			self.out.write(self.arith[command]+'\n')
		else:
			self.out.write(command.lower()+'\n')

	#--------------------------------------------------------------------------
	# This writes a lable
	def writeLabel(self, label):
		self.out.write('label '+label+'\n')

	#--------------------------------------------------------------------------
	# This writes a gotto
	def writeGoto(self, label):
		self.out.write('goto '+label+'\n')

	#--------------------------------------------------------------------------
	# This writes an if statement
	def writeIf(self,label):
		self.out.write('if-goto '+label+'\n')

	#--------------------------------------------------------------------------
	# This writes a function call
	def writeCall(self,name,nArgs):
		self.out.write('call '+name+' '+repr(nArgs)+'\n')

	#--------------------------------------------------------------------------
	# This writes a function delceration
	def writeFunction(self,name,nLocals):
		self.out.write('function '+name+' '+repr(nLocals)+'\n')

	#--------------------------------------------------------------------------
	# This writes a return
	def writeReturn(self):
		self.out.write('return\n')

	#--------------------------------------------------------------------------
	# This closes the output
	def close(self):
		self.out.close()