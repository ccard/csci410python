import sys, string, os, io,re
#------------------------------------------------------------------------------
#Chris Card
#CS410
#ECS project 07
#python 3.3
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

	#The current file being parsed
	fileName=''


	#jump counters
	eq_jump=0
	lt_jump=0
	gt_jump=0

	#Table for translating locations
	locat = {'local':'LCL', 'argument':'ARG','this':'THIS',
			'that':'THAT', 'pointer':'3', 'temp':'5', 'static':'16'}

	#Table for function return counts
	functRetC = {'i':0}


	#--------------------------------------------------------------------------
	# The constructor
	def __init__(self, fileout):
		self.outfile = open(fileout, 'w')
		

	#--------------------------------------------------------------------------
	# Closes the current file
	def Close(self):
		self.outfile.close()

	#--------------------------------------------------------------------------
	# This sets the filename to the new file being parsed
	def setFileName(self, fileout):
		self.fileName = fileout

	#--------------------------------------------------------------------------
	# This bootstraps the flie i.e. initializing the sp pointer and calling
	# sys.init
	def writeInit(self):
		temp_s = '//Bootstrapping\n'
		temp_s += '@256\n'
		temp_s += 'D=A\n\n'
		temp_s += '@SP\n'
		temp_s += 'M=D\n\n'
		self.outfile.write(temp_s)
		self.writeCall('Sys.init','0')

	#--------------------------------------------------------------------------
	# This writes a label to the file with file name prepended to make more
	# unique
	def writeLabel(self, label):
		temp_s = '('+self.fileName+'.'+label+')\n\n'
		self.outfile.write(temp_s)

	#--------------------------------------------------------------------------
	# This grites a goto statement or a mandatory jump
	def writeGoto(self,label):
		temp_s = '@'+self.fileName+'.'+label+'\n'
		temp_s += '0;JMP\n\n'
		self.outfile.write(temp_s)

	#--------------------------------------------------------------------------
	# This writes a if-goto statment when the element on the top of the
	# stack is not 0
	def writeIf(self,label):
		temp_s = '//if statment\n'
		temp_s += '@SP\n'
		temp_s += 'M=M-1\n'
		temp_s += 'A=M\n'
		temp_s += 'D=M\n\n'
		temp_s += '@'+self.fileName+'.'+label+'\n'
		temp_s += 'D;JNE\n\n'
		self.outfile.write(temp_s)

	#--------------------------------------------------------------------------
	# This writes the call of a function with number of arguments to pass to 
	# it and saves all relvent pointers to the stack and then resets
	# SP to the new location for the function
	def writeCall(self, functionName, numArgs):
		#This keeps count of the number of returns of a function to
		#ensure that it returns to the proper place in code
		temp = 0
		if functionName in self.functRetC:
			temp = self.functRetC[functionName]
			self.functRetC[functionName] = temp+1
		else:
			self.functRetC[functionName] = temp+1

		ret = functionName+'.RET.'+repr(temp)

		temp_s = "//calls function "+functionName+'\n'
		self.outfile.write(temp_s)
		#pushes return value onto the stack
		self.writePushPop(self.push_type,'constant',ret)
		temp_s = '//saves local to stack\n'
		temp_s += "@LCL\n"
		temp_s += "D=M\n\n"
		temp_s += "@SP\n"
		temp_s += "AM=M+1\n"
		temp_s += "A=A-1\n"
		temp_s += "M=D\n\n"
		
		temp_s += '//saves arg to the stack\n'
		temp_s += "@ARG\n"
		temp_s += "D=M\n\n"
		temp_s += "@SP\n"
		temp_s += "AM=M+1\n"
		temp_s += "A=A-1\n"
		temp_s += "M=D\n\n"
		
		temp_s += '//saves this to stack\n'
		temp_s += "@THIS\n"
		temp_s += "D=M\n\n"
		temp_s += "@SP\n"
		temp_s += "AM=M+1\n"
		temp_s += "A=A-1\n"
		temp_s += "M=D\n\n"

		temp_s += '//saves that to stack\n'
		temp_s += "@THAT\n"
		temp_s += "D=M\n\n"
		temp_s += "@SP\n"
		temp_s += "AM=M+1\n"
		temp_s += "A=A-1\n"
		temp_s += "M=D\n\n"

		temp_s += '//resets arg to new location\n'
		temp_s += '@SP\n'
		temp_s += 'D=M\n\n'
		temp_s += '@'+numArgs+'\n'
		temp_s += 'D=D-A\n\n'
		temp_s += '@5\n'
		temp_s += 'D=D-A\n\n'
		temp_s += '@ARG\n'
		temp_s += 'M=D\n\n'

		temp_s += '//sets lcl to sp\n'
		temp_s += '@SP\n'
		temp_s += 'D=M\n\n'
		temp_s += '@LCL\n'
		temp_s += 'M=D\n\n'

		temp_s += '@'+functionName+'\n'
		temp_s += '0;JMP\n\n'

		temp_s += '('+ret+')\n\n'

		#if it is the call to sys.init then at the begining of file
		#and need to make sure to goto the infinite while loop at the
		#end and not repeate code
		if 'Sys.init' in functionName:
			temp_s += '@Sys.WHILE\n'
			temp_s += '0;JMP\n\n'

		self.outfile.write(temp_s)

	#--------------------------------------------------------------------------
	# This writes the return call of the function
	def writeReturn(self):
		temp_s = '//return frame of the function\n'
		temp_s += '@LCL\n'
		temp_s += 'D=M\n\n'
		temp_s += '@R13\n'
		temp_s += 'MD=D\n\n'

		temp_s += '//gets the return address\n'
		temp_s += '@5\n'
		temp_s += 'D=D-A\n'
		temp_s += 'A=D\n'
		temp_s += 'D=M\n\n'
		temp_s += '@R14\n'
		temp_s += 'M=D\n\n'

		temp_s += '//moves return value to arg\n'
		temp_s += '@SP\n'
		temp_s += 'M=M-1\n'
		temp_s += 'A=M\n'
		temp_s += 'D=M\n\n'
		temp_s += '@ARG\n'
		temp_s += 'A=M\n'
		temp_s += 'M=D\n\n'

		temp_s += '//repositions the stack pointer for caller\n'
		temp_s += '@ARG\n'
		temp_s += 'D=M\n\n'
		temp_s += '@SP\n'
		temp_s += 'M=D+1\n\n'

		temp_s += '//resets that to the caller\n'
		temp_s += '@R13\n'
		temp_s += 'D=M\n\n'
		temp_s += '@1\n'
		temp_s += 'D=D-A\n'
		temp_s += 'A=D\n'
		temp_s += 'D=M\n\n'
		temp_s += '@THAT\n'
		temp_s += 'M=D\n\n'

		temp_s += '//resets this to the caller\n'
		temp_s += '@R13\n'
		temp_s += 'D=M\n\n'
		temp_s += '@2\n'
		temp_s += 'D=D-A\n'
		temp_s += 'A=D\n'
		temp_s += 'D=M\n\n'
		temp_s += '@THIS\n'
		temp_s += 'M=D\n\n'

		temp_s += '//resets arg to the caller\n'
		temp_s += '@R13\n'
		temp_s += 'D=M\n\n'
		temp_s += '@3\n'
		temp_s += 'D=D-A\n'
		temp_s += 'A=D\n'
		temp_s += 'D=M\n\n'
		temp_s += '@ARG\n'
		temp_s += 'M=D\n\n'

		temp_s += '//resets lcl to the caller\n'
		temp_s += '@R13\n'
		temp_s += 'D=M\n\n'
		temp_s += '@4\n'
		temp_s += 'D=D-A\n'
		temp_s += 'A=D\n'
		temp_s += 'D=M\n\n'
		temp_s += '@LCL\n'
		temp_s += 'M=D\n\n'

		temp_s += '//returns to the calling function\n'
		temp_s += '@R14\n'
		temp_s += 'D=M\n\n'
		temp_s += '@0\n'
		temp_s += 'A=D\n'
		temp_s += '0;JMP\n\n'

		self.outfile.write(temp_s)

	#--------------------------------------------------------------------------
	# This wirtes the code for a function label
	def writeFunction(self, functionName, numLocals):
		temp = int(numLocals)
		self.currFunct = functionName
		self.outfile.write('('+functionName+')\n\n')
		self.outfile.write('//zero local values\n')
		#loops through numLocals times to 0 out the lcl block
		#and to position the sp to the new location after lcl block
		for i in range(0,temp):
			self.writePushPop(self.push_type,'constant','0')


	#--------------------------------------------------------------------------
	# Writes arithmatic commands
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
	# Writes appropriate push pop commands
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
				if 'static' in segment:
					temp_s += "@"+self.fileName+"$static."+index+"\n"
					temp_s += "D=M\n\n"
					temp_s += "@SP\n"
					temp_s += "AM=M+1\n"
					temp_s += "A=A-1\n"
					temp_s += "M=D\n\n"
					self.outfile.write(temp_s)

				elif 'temp' in segment or 'pointer' in segment:
					temp_s += "@"+index+"\n"
					temp_s += "D=A\n\n"
					temp_s += "@"+self.locat[segment]+"\n"
					temp_s += "A=D+A\n"
					temp_s += "D=M\n\n"
					temp_s += "@SP\n"
					temp_s += "AM=M+1\n"
					temp_s += "A=A-1\n"
					temp_s += "M=D\n\n"
					self.outfile.write(temp_s)

				else:
					temp_s += "@"+index+"\n"
					temp_s += "D=A\n\n"
					temp_s += "@"+self.locat[segment]+"\n"
					temp_s += "A=D+M\n"
					temp_s += "D=M\n\n"
					temp_s += "@SP\n"
					temp_s += "AM=M+1\n"
					temp_s += "A=A-1\n"
					temp_s += "M=D\n\n"
					self.outfile.write(temp_s)

		else:
			temp_s = "//This is the pop command\n"
			#pops constant off stack which is just modifing sp = sp-1
			if 'constant' in segment:
				temp_s += "@SP\n"
				temp_s += "M=M-1\n\n"
				self.outfile.write(temp_s)
			else:
				if 'static' in segment:
					temp_s += "@SP\n"
					temp_s += "M=M-1\n"
					temp_s += "A=M\n"
					temp_s += "D=M\n\n"
					temp_s += "@"+self.fileName+"$static."+index+"\n"
					temp_s += "M=D\n\n"
					self.outfile.write(temp_s)

				elif 'temp' in segment or 'pointer' in segment:
					temp_s += "@"+index+"\n"
					temp_s += "D=A\n\n"
					temp_s += "@"+self.locat[segment]+"\n"
					temp_s += "D=D+A\n"
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

				else:
					temp_s += "@"+index+"\n"
					temp_s += "D=A\n\n"
					temp_s += "@"+self.locat[segment]+"\n"
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
