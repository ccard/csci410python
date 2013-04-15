import sys, string, os, io,re
from jacktokenizer import JackToken
from symboltable import SymbolTable
from vmwriter import VMWriter
#------------------------------------------------------------------------------
#Chris Card
#CS410
#ECS project 10
#python 3.3
#Due:3/25/13
#This file compiles the input into actual code
#------------------------------------------------------------------------------

class CompilationEngine:
	#------------------------------------------------------------------------------
	# Var Declar:
	#------------------------------------------------------------------------------
	
	#stores all the different key words
	key_class='CLASS'
	key_method='METHOD'
	key_function='FUNCTION'
	key_constructor='CONSTRUCTOR'
	key_int='INT'
	key_boolean='BOOLEAN'
	key_char='CHAR'
	key_void='VOID'
	key_var='VAR'
	key_static='STATIC'
	key_field='FIELD'
	key_let='LET'
	key_do='DO'
	key_if='IF'
	key_else='ELSE'
	key_while='WHILE'
	key_return='RETURN'
	key_true='TRUE'
	key_false='FALSE'
	key_null='NULL'
	key_this='THIS'
	
	#stores all the token types
	keyword='KEYWORD'
	sym='SYMBOL'
	ident='IDENTIFIER'
	intc='INT_CONST'
	string_c='STRING_CONST'

	segment = {'VAR':'local', 'STATIC':'static', 'FIELD':'this', 'ARG':'argument'}

	loopCounter = 0
	ifCounter = 0

	#--------------------------------------------------------------------------
	# Class declaration:
	#--------------------------------------------------------------------------

	#------------------------------------------------------------------------------
	# This is the constructor
	def __init__(self,infile,outfile):
		self.writer = VMWriter(outfile)
		self.token = JackToken(infile)
		self.table = SymbolTable()
	
	#------------------------------------------------------------------------------
	# This method compiles the entire class contained in the input file
	def compileClass(self):
		self.token.advance()

		while self.token.hasMoreTokens():
			tokentype = self.token.tokenType()

			if self.keyword in tokentype:
				tempkey = self.token.keyWord()
				if self.key_class in tempkey:
					s = "nothing to do here"
				
				#if the keyword is static or field then it is known that it is a class var dec
				#at this level of compilation
				elif self.key_static in tempkey or self.key_field in tempkey:
					self.compileClassVarDec()
					continue #continue because there maybe more then one class var and don't want to advane tokenizer

				#if the keyword is a subroutine type
				elif self.key_constructor in tempkey or self.key_method in tempkey or self.key_function in tempkey:
					self.compileSubroutine()

			elif self.sym in tokentype:
				tempsym = self.token.symbol()

				#if we run into } at this level then we are at the end of the class
				if '}' in tempsym:
					break


			elif self.ident in tokentype:
				tempident = self.token.identifier()
				self.currClassName = tempident

			self.token.advance()

		self.writer.close()

	#------------------------------------------------------------------------------
	# This method compiles class var dec
	def compileClassVarDec(self):
		curtype = ""
		curkind = ""
		curname = ""

		while self.token.hasMoreTokens:
			tokentype = self.token.tokenType()

			if self.keyword in tokentype:
				tempkey = self.token.keyWord()

				if self.key_int in tempkey or self.key_char in tempkey or self.key_boolean in tempkey:
					curtype = tempkey

				elif self.key_static in tempkey or self.key_field in tempkey:
					curkind = tempkey

				#if we run into a subroutine declaration then we break
				elif self.key_function in tempkey or self.key_method in tempkey or self.key_constructor in tempkey:
					break
					
			elif self.ident in tokentype:
				tempident = self.token.identifier()
				if len(curtype) == 0:
					curtype = tempident
				else:
					curname = tempident

			elif self.sym in tokentype:
				tempsym = self.token.symbol()

				#if it runs into any of the below symboles then it is an invalid var decleration
				if re.search('[\(\)\{\}\[\]\.\+\-\*\/\&\<\>\=\~]{1}',tempsym) is not None:
					print(self.token.errorMsg())
					sys.exit(0)

				#if we run into a ; then it is the end of this particular class var dec
				if ';' in tempsym:
					self.token.advance()
					self.table.Define(curname,curtype,curkind)
					break

				self.table.Define(curname,curtype,curkind)
				curname = ''

			self.token.advance()

	#------------------------------------------------------------------------------
	# This method compiles the subroutines
	def compileSubroutine(self):
		self.table.startSubroutine()
		self.curSubType = ''
		if_param = False #ensures that at least an empty param list is discovered

		self.isConstruct = False

		isFunct = False

		while self.token.hasMoreTokens:
			tokentype = self.token.tokenType()

			if self.keyword in tokentype:
				tempkey = self.token.keyWord()

				if self.key_method in tempkey or self.key_function in tempkey or self.key_constructor in tempkey:
					self.isConstruct = True if self.key_constructor in tempkey else False
					isFunct = True if self.key_function in tempkey else False

				elif self.key_int in tempkey or self.key_char in tempkey or self.key_boolean in tempkey or self.key_void in tempkey:
					self.curSubType = tempkey

				#if the keyward var is in tempkey then we need to compile a vardeck
				elif self.key_var in tempkey:
					self.compileVarDec()

				#if it runs into any keywords that aren't caught by the above statements then it is no longer
				#in a subroutine
				else:
					self.writer.writeFunction(self.currClassName+'.'+self.curSubName,self.table.varCount('VAR'))
					break

			elif self.sym in tokentype:
				tempsym = self.token.symbol()

				#if it runs into a ( then it is descovering a parameter list
				if '(' in tempsym:
					self.token.advance()
					#compiles the parameter list
					self.compileParameterList(self.isConstruct or isFunct)

					if_param = True #set param list discovered to true

				#if it has fond at lest an empty paramlist then it can print the next symboles 
				elif if_param:
					s = "this is does nothing just place holeder"

				#error
				else:
					print(self.token.errorMsg())
					sys.exit(0)

			elif self.ident in tokentype:
				if len(self.curSubType) == 0:
					self.curSubType = self.token.identifier()

				else:
					self.curSubName = self.token.identifier()

			self.token.advance()

		if 'NONE' not in self.table.kindOf('this'):
			self.writer.writePush(self.segment[self.table.kindOf('this')],repr(self.table.indexOf('this')))
			self.writer.writePop('pointer','0')

		if self.isConstruct:
			self.writer.writePush('constant',repr(self.table.varCount('FIELD')))
			self.writer.writeCall('Memory.alloc',1)
			self.writer.writePop('pointer','0')

		self.compileStatements()

		self.loopCounter = 0
		self.ifCounter = 0
		self.curSubName = ''

	#------------------------------------------------------------------------------
	# This method compiles the parameter list
	def compileParameterList(self,isConstruct):
		curname = ''
		curtype = ''
		curkind = ''

		if not isConstruct:
			self.table.Define('this',self.currClassName,'ARG')

		while self.token.hasMoreTokens():
			tokentype = self.token.tokenType()

			if self.keyword in tokentype:
				tempkey = self.token.keyWord()
				curtype = tempkey

			elif self.ident in tokentype:
				tempident = self.token.identifier()
				if len(curtype) == 0:
					curtype = tempident
				else:
					curname = tempident

			elif self.sym in tokentype:
				tempsym = self.token.symbol()

				#if it runs into a ) means the end of the parameter list so break
				if ')' in tempsym:
					self.table.Define(curname, curtype, 'ARG')
					break

				#seperation of the parameters
				elif ',' in tempsym:
					self.table.Define(curname, curtype, 'ARG')
					curname = ''
					curtype = ''

				#any other symbol results in a an error
				else:
					print(self.token.errorMsg())
					sys.exit(0)
			
			self.token.advance()
		
		#advance twice because we are at ( so need to getpast that and need to get the next symbol
		self.token.advance()
		self.token.advance()

	#------------------------------------------------------------------------------
	# This method compiles the var decliration
	def compileVarDec(self):
		curname = ''
		curtype = ''

		while self.token.hasMoreTokens():
			tokentype = self.token.tokenType()

			if self.keyword in tokentype:
				tempkey = self.token.keyWord()

				if self.key_var in tempkey:
					s = 'Place holder does nothing just ensures that a var is seen'

				elif self.key_int in tempkey or self.key_char in tempkey or self.key_boolean in tempkey:
					curtype = tempkey

				#if any keyword is docovered than what is above then the vardec is over
				else:
					break

			elif self.ident in tokentype:
				tempident = self.token.identifier()
				if len(curtype) == 0:
					curtype = tempident
				else:
					curname = tempident

			elif self.sym in tokentype:
				tempsym = self.token.symbol()

				if ',' in tempsym:
					self.table.Define(curname,curtype, 'VAR')
					curname = ''

				#once ; is found then at the end of a vardec
				elif ';' in tempsym:
					self.table.Define(curname,curtype, 'VAR')
					break

			self.token.advance()

	#------------------------------------------------------------------------------
	# This method compiles the statements
	def compileStatements(self):

		while self.token.hasMoreTokens():
			tokentype = self.token.tokenType()

			if self.keyword in tokentype:
				tempkey = self.token.keyWord()

				#if 'let' is found then compilelet
				if self.key_let in tempkey:
					self.compileLet()

				elif self.key_if in tempkey:
					self.compileIf()
					
					#continue because we could have multiple if statements found and
					#the current token could be the key word if so we don't want to advance
					#the tokenizer prematurely
					continue

				elif self.key_while in tempkey:
					self.compileWhile()

				elif self.key_do in tempkey:
					self.compileDo()

				elif self.key_return in tempkey:
					self.compileReturn()

				#incorrect key word at this level of compilation
				else:
					print(self.token.errorMsg())
					sys.exit(0)

			elif self.sym in tokentype:
				tempsym = self.token.symbol()
				#once we run into } thats the endof statments
				if '}' in tempsym:
					break
				#any other symbol discovered at this stage is an error
				else:
					print(self.token.errorMsg())
					sys.exit(0)

			self.token.advance()

	#------------------------------------------------------------------------------
	# This method compiles the do 
	def compileDo(self):
	
		while self.token.hasMoreTokens():
			tokentype = self.token.tokenType()

			if self.keyword in tokentype:
				tempkey = self.token.keyWord()

				if self.key_do in tempkey:
					s = 'Place holder this does nothing'

				#if any keyword other then do is discovered at this level it results in an error
				else:
					print(self.token.errorMsg())
					sys.exit(0)

			elif self.ident in tokentype:
				#compiles the expression with the value for a subroutine call passed in being true
				self.compileExpression(True)
				
				self.token.advance()
				break

			self.token.advance()

		self.writer.writePop('temp','0')
		
	#------------------------------------------------------------------------------
	# This method compiles the letStatement
	def compileLet(self):
		isArray = False

		leftSideEq = ''

		while self.token.hasMoreTokens():
			tokentype = self.token.tokenType()

			if self.keyword in tokentype:
				tempkey = self.token.keyWord()

				if self.key_let in tempkey:
					s = 'Place holder this does nothing'

				#if any other keyword is discovered it is an error
				else:
					print(self.token.errorMsg())
					sys.exit(0)

			elif self.ident in tokentype:
				tempident = self.token.identifier()
				peak = self.token.peak()
				#if [ is discovered it means that it is an array access
				if '[' in peak:
					self.token.advance()
					self.token.advance()

					kind = self.table.kindOf(tempident)

					if "NONE" in kind:
						print(self.token.errorMsg()+"Undefined Variable\n")
						sys.exit(0)

					self.writer.writePush(self.segment[kind],repr(self.table.indexOf(tempident)))

					self.compileExpression(False)

					self.writer.writeArithmetic('+')

					isArray = True
			
					self.token.advance()
					#continue so that the bellow error catching isn't accidently triped hence the advance command
					#before this
					continue

				else:
					kind = self.table.kindOf(tempident)

					if "NONE" in kind:
						print(self.token.errorMsg()+"Undefined Variable\n")
						sys.exit(0)

					leftSideEq = tempident

			elif self.sym in tokentype:
				tempsym = self.token.symbol()

				#this means that we compile th expression on the other side of the = sign
				if '=' in tempsym:
					self.token.advance()
					self.compileExpression(False)

					if isArray:
						self.writer.writePop('temp','0')
						self.writer.writePop('pointer','1')
						self.writer.writePush('temp','0')
						self.writer.writePop('that','0')

					else:
						kind = self.table.kindOf(leftSideEq)
						self.writer.writePop(self.segment[kind],repr(self.table.indexOf(leftSideEq)))

					#sets tempsym to the current symbole
					tempsym = self.token.symbol()
				
				#if tempsym at this point is ; then end of let statement
				if ';' in self.token.symbol():
					break

				#othre wise it is an error
				else:
					print(self.token.errorMsg())
					sys.exit(0)

			self.token.advance()

	#------------------------------------------------------------------------------
	# This method compiles the whileStatement
	def compileWhile(self):
		curLoop = self.curSubName+'.loop.'+repr(self.loopCounter)
		curLoopExit = curLoop+'.EXIT'
		self.loopCounter += 1

		while self.token.hasMoreTokens():
			tokentype = self.token.tokenType()

			if self.keyword in tokentype:
				tempkey = self.token.keyWord()

				if self.key_while in tempkey:
					self.writer.writeLabel(curLoop)
				
				#if any other keyword is discovered at this level it is an error
				else:
					print(self.token.errorMsg())
					sys.exit(0)

			elif self.sym in tokentype:
				tempsym = self.token.symbol()

				#the condition of the while loop
				if '(' in tempsym:
					self.token.advance()
					self.compileExpression(False)
					self.writer.writeArithmetic('~')
					self.writer.writeIf(curLoopExit)

				#body of the while loop
				elif '{' in tempsym:
					self.token.advance()
					self.compileStatements()
					self.writer.writeGoto(curLoop)
					#once the statments are compiled the whilestatment is done
					break

				#any other symbol at this level results in an error
				else:
					print(self.token.errorMsg())
					sys.exit(0)

			self.token.advance()

		self.writer.writeLabel(curLoopExit)

	#------------------------------------------------------------------------------
	# This method compiles the ReturnStatement
	def compileReturn(self):

		while self.token.hasMoreTokens():
			tokentype = self.token.tokenType()

			if self.keyword in tokentype:
				tempkey = self.token.keyWord()

				if self.key_return in tempkey:
					s = "Place holder does nothing"

				#Any other keyword means that an exprssion is to be compiled and return is done
				else:
					self.compileExpression(False)
					self.token.advance()
					break

			#other wise compile expression
			elif self.ident in tokentype or self.string_c in tokentype or self.intc in tokentype:
				self.compileExpression(False)
				self.token.advance()
				break

			elif self.sym in tokentype:
				tempsym = self.token.symbol()

				#denotes the end of a return statment
				if ';' in tempsym:
					if self.curSubType == self.currClassName:
						self.writer.writePush('pointer','0')

					elif self.key_void not in self.curSubType:
						print(self.token.errorMsg()+'must return something\n')
						sys.exit(0)

					else:
						self.writer.writePush('constant','0')

					break
				#any other symbol at this level is an error
				else:
					print(self.token.errorMsg())
					sys.exit(0)

			self.token.advance()

		self.writer.writeReturn()
		
	#------------------------------------------------------------------------------
	# This method compiles the ifStatement
	def compileIf(self):
		currIf = self.curSubName+'.else.'+repr(self.ifCounter)
		currIfExit = self.curSubName+'.if.'+repr(self.ifCounter)+'.EXIT'
		self.ifCounter += 1

		ifElse = False

		#this means that keyword if has been seen only once so if it seen again
		#that means it is a seperate if statment 
		seen_once = True

		while self.token.hasMoreTokens():
			tokentype = self.token.tokenType()

			if self.keyword in tokentype:
				tempkey = self.token.keyWord()

				if self.key_if in tempkey and seen_once:
					s = 'Place holeder does nothing'

				elif self.key_else in tempkey and not ifElse:
					ifElse = True
					self.writer.writeGoto(currIfExit)
					self.writer.writeLabel(currIf)

				#if any other keyword is seen then it is the end of an if statement
				else:
					break

			elif self.sym in tokentype:
				tempsym = self.token.symbol()

				#The condition of an if statment
				if '(' in tempsym:
					self.token.advance()
					self.compileExpression(False)
					self.writer.writeArithmetic('~')
					self.writer.writeIf(currIf)

				#body of an if|else statment
				elif '{' in tempsym:
					self.token.advance()
					self.compileStatements()
					seen_once = False
					if ifElse:
						self.token.advance()
						break

				#just incase this catches } which means that its
				#the end of an if else block that isn't this one
				elif '}' in tempsym:
					break

			self.token.advance()

		if ifElse:
			self.writer.writeLabel(currIfExit)

		else:
			self.writer.writeLabel(currIf)

	#------------------------------------------------------------------------------
	# This method compiles the expression
	def compileExpression(self,enclosed):

		while self.token.hasMoreTokens():
			tokentype = self.token.tokenType()

			if self.sym in tokentype:
				tempsym = self.token.symbol()

				#this means that we have term to compile
				if tempsym in '(~-':
					self.compileTerm(enclosed,True,False,'')

				#signifies the end of an expression
				elif tempsym in ';)],':
					break

			else:
				self.compileTerm(enclosed,False,False,'')

			self.token.advance()

	#------------------------------------------------------------------------------
	# This method compiles the term
	def compileTerm(self,enclosed,isUnary,callfromTerm,prevSym):

		while self.token.hasMoreTokens():
			tokentype = self.token.tokenType()

			if self.keyword in tokentype:
				tempkey = self.token.keyWord()

				if self.key_true in tempkey:
					self.writer.writePush('constant','1')
					self.writer.writeArithmetic('NEG')

				elif self.key_false in tempkey:
					self.writer.writePush('constant','0')

				elif self.key_null in tempkey:
					self.writer.writePush('constant','0')

				elif self.key_this in tempkey:
					self.writer.writePush('pointer','0')
					
				
				#any other keyword than the ones above results in an error
				else:
					print(self.token.errorMsg())
					sys.exit(0)

			elif self.ident in tokentype:
				tempident = self.token.identifier()
				#peaks at the next token to determine the type of call
				peaks = self.token.peak()

				#means that it as a call to a var or class method
				if '.' in peaks:
					callName = ''
					numArgs = 0
					#replace this with code to do a look up
					typeof = self.table.typeOf(tempident)
					if 'NONE' in typeof:
					 	callName = tempident

					else:
					 	callName = typeof
					 	numArgs += 1
					 	self.writer.writePush(self.segment[self.table.kindOf(tempident)],repr(self.table.indexOf(tempident)))

					self.token.advance()

					callName += self.token.symbol()

					self.token.advance()

					if self.ident in self.token.tokenType():
						callName += self.token.identifier()

					else:
						print(self.token.errorMsg())
						sys.exit(0)
					
					self.token.advance()

					if self.sym not in self.token.tokenType():
						print(self.token.errorMsg())
						sys.exit()

					self.token.advance()

					#then compiles the expression list
					numArgs += self.compileExpressionList()

					self.writer.writeCall(callName,numArgs)

				#this means that it is a subroutine call to one of its own methods
				elif '(' in peaks:
					self.writer.writePush('pointer','0')
					
					self.token.advance()
					self.token.advance()

					numArgs = self.compileExpressionList()+1

					self.writer.writeCall(self.currClassName+'.'+tempident,numArgs if numArgs != 0 else 1)

				#this means that it is accessing an array element
				elif '[' in peaks:
					self.token.advance()
					self.token.advance()
					kind = self.table.kindOf(tempident)

					if "NONE" in kind:
						print(self.token.errorMsg()+"Undefined Variable\n")
						sys.exit(0)

					self.writer.writePush(self.segment[kind],repr(self.table.indexOf(tempident)))

					self.compileExpression(enclosed)

					self.writer.writeArithmetic('+')

					self.writer.writePop('pointer','1')
					
					self.writer.writePush('that','0')

				#other wise it is just an identifier
				else:
					kind = self.table.kindOf(tempident)

					if "NONE" in kind:
						print(self.token.errorMsg()+"Undefined Variable\n")
						sys.exit(0)

					self.writer.writePush(self.segment[kind],repr(self.table.indexOf(tempident)))

			elif self.intc in tokentype:
				self.writer.writePush('constant',self.token.intVal())

			elif self.string_c in tokentype:
				string = self.token.stringVal()
				self.writer.writePush('constant', repr(len(string)))
				self.writer.writeCall('String.new',1)
				for c in string:
					self.writer.writePush('constant',repr(ord(c)))
					self.writer.writeCall('String.appendChar',2)

			elif self.sym in tokentype:
				tempsym = self.token.symbol()

				#this means that it is and expression surrounded by ()
				if '(' in tempsym:
					self.token.advance()
					self.compileExpression(True)
					enclosed = True

				#not unary operator 
				elif '~' in tempsym:
					self.token.advance()

					self.compileTerm(enclosed,False,False,prevSym)

					self.writer.writeArithmetic(tempsym)

				elif '-' in tempsym and isUnary and not enclosed:
					self.token.advance()

					self.compileTerm(enclosed,False,False,prevSym)

					self.writer.writeArithmetic('NEG')

				#operator
				elif tempsym in '+-*/&|<>=':
					self.token.advance()

					if callfromTerm:
						if '*' in prevSym:
							self.writer.writeCall('Math.multiply',2)

						elif '/' in prevSym:
							self.writer.writeCall('Math.divide',2)

						else:
							self.writer.writeArithmetic(prevSym)

					self.compileTerm(enclosed,False,True,tempsym)

					if not callfromTerm:
						if '*' in tempsym:
							self.writer.writeCall('Math.multiply',2)
	
						elif '/' in tempsym:
							self.writer.writeCall('Math.divide',2)
	
						else:
							self.writer.writeArithmetic(tempsym)
					
			#if the next token is ]);, means the end of a term
			if self.token.peak() in ']);,':
				break

			self.token.advance()

	#------------------------------------------------------------------------------
	# This method compiles the expressionList
	def compileExpressionList(self):
		expressCount = 0

		while self.token.hasMoreTokens():
			tokentype = self.token.tokenType()

			if self.sym in tokentype:
				tempsym = self.token.symbol()

				#indicates teh start of another expression
				if ',' in tempsym:
					self.token.advance()

					self.compileExpression(False)

					expressCount += 1

				#indicates that end of expression list
				elif ')' in tempsym:
					break

				else:
					self.compileExpression(False)
					expressCount += 1
			else:
				self.compileExpression(False)
				expressCount += 1

		return expressCount

#-------------------End Class--------------------------------------------------