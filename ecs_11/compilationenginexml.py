import sys, string, os, io,re
from jacktokenizer import JackToken
from symboltable import SymbolTable
#------------------------------------------------------------------------------
#Chris Card
#CS410
#ECS project 10
#python 3.3
#Due:3/25/13
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

	#for off setting the xml attributes in the output file
	space = ' '
	spaceCount = 0
	
	#look up table for xml attributes
	xml={'classb':'<class>','classe':'</class>','classVarDecb':'<classVarDec>','classVarDece':'</classVarDec>'
		,'subroutineDecb':'<subroutineDec>','subroutineDece':'</subroutineDec>','parameterListb':'<parameterList>','parameterListe':'</parameterList>'
		,'subroutineBodyb':'<subroutineBody>','subroutineBodye':'</subroutineBody>','varDecb':'<varDec>','varDece':'</varDec>'
		,'statementsb':'<statements>','statementse':'</statements>','letStatementb':'<letStatement>','letStatemente':'</letStatement>'
		,'ifStatementb':'<ifStatement>','ifStatemente':'</ifStatement>','whileStatementb':'<whileStatement>','whileStatemente':'</whileStatement>'
		,'doStatementb':'<doStatement>','doStatemente':'</doStatement>','ReturnStatementb':'<returnStatement>','ReturnStatemente':'</returnStatement>'
		,'expressionb':'<expression>','expressione':'</expression>','termb':'<term>','terme':'</term>','expressionListb':'<expressionList>'
		,'expressionListe':'</expressionList>','integerConstantb':'<integerConstant>','integerConstante':'</integerConstant>','StringConstantb':'<stringConstant>'
		,'StringConstante':'</stringConstant>','identifierb':'<identifier>','identifiere':'</identifier>','keywordb':'<keyword>','keyworde':'</keyword>',
		'symbolb':'<symbol>', 'symbole':'</symbol>'}
	
	#--------------------------------------------------------------------------
	# Class declaration:
	#--------------------------------------------------------------------------

	#------------------------------------------------------------------------------
	# This is the constructor
	def __init__(self,infile,outfile):
		self.of = open(outfile,'w')
		self.token = JackToken(infile)
		self.table = SymbolTable()
	
	#------------------------------------------------------------------------------
	# This method compiles the entire class contained in the input file
	def compileClass(self):
		self.of.write((self.space*self.spaceCount)+self.xml['classb']+'\n')
		self.spaceCount += 1
		self.token.advance()

		while self.token.hasMoreTokens():
			tokentype = self.token.tokenType()

			if self.keyword in tokentype:
				tempkey = self.token.keyWord()
				if self.key_class in tempkey:
					self.of.write((self.space*self.spaceCount)+self.xml['keywordb']+tempkey.lower()+self.xml['keyworde']+'\n')
				
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
					self.of.write((self.space*self.spaceCount)+self.xml['symbolb']+tempsym+self.xml['symbole']+'\n')
					break

				self.of.write((self.space*self.spaceCount)+self.xml['symbolb']+tempsym+self.xml['symbole']+'\n')

			elif self.ident in tokentype:
				tempident = self.token.identifier()
				self.currClassName = tempident
				self.of.write((self.space*self.spaceCount)+self.xml['identifierb']+tempident+self.xml['identifiere']+'\n')

			self.token.advance()

		self.spaceCount -= 1
		self.of.write((self.space*self.spaceCount)+self.xml['classe'])
		self.of.close()

	#------------------------------------------------------------------------------
	# This method compiles class var dec
	def compileClassVarDec(self):
		self.of.write((self.space*self.spaceCount)+self.xml['classVarDecb']+'\n')
		self.spaceCount += 1

		curtype = ""
		curkind = ""
		curname = ""

		while self.token.hasMoreTokens:
			tokentype = self.token.tokenType()

			if self.keyword in tokentype:
				tempkey = self.token.keyWord()

				if self.key_int in tempkey or self.key_char in tempkey or self.key_boolean in tempkey:
					curtype = tempkey
					self.of.write((self.space*self.spaceCount)+self.xml['keywordb']+tempkey.lower()+self.xml['keyworde']+'\n')

				elif self.key_static in tempkey or self.key_field in tempkey:
					curkind = tempkey
					self.of.write((self.space*self.spaceCount)+self.xml['keywordb']+tempkey.lower()+self.xml['keyworde']+'\n')

				#if we run into a subroutine declaration then we break
				elif self.key_function in tempkey or self.key_method in tempkey or self.key_constructor in tempkey:
					break
					
			elif self.ident in tokentype:
				tempident = self.token.identifier()
				if len(curtype) == 0:
					curtype = tempident
				else:
					curname = tempident
				self.of.write((self.space*self.spaceCount)+self.xml['identifierb']+tempident+self.xml['identifiere']+'\n')

			elif self.sym in tokentype:
				tempsym = self.token.symbol()

				#if it runs into any of the below symboles then it is an invalid var decleration
				if re.search('[\(\)\{\}\[\]\.\+\-\*\/\&\<\>\=\~]{1}',tempsym) is not None:
					print(self.token.errorMsg())
					sys.exit(0)

				#if we run into a ; then it is the end of this particular class var dec
				if ';' in tempsym:
					self.of.write((self.space*self.spaceCount)+self.xml['symbolb']+tempsym+self.xml['symbole']+'\n')
					self.token.advance()
					self.table.Define(curname,curtype,curkind)
					break
				self.table.Define(curname,curtype,curkind)
				curname = ''
				self.of.write((self.space*self.spaceCount)+self.xml['symbolb']+tempsym+self.xml['symbole']+'\n')

			self.token.advance()

		self.spaceCount -= 1
		self.of.write((self.space*self.spaceCount)+self.xml['classVarDece']+'\n')

	#------------------------------------------------------------------------------
	# This method compiles the subroutines
	def compileSubroutine(self):
		self.of.write((self.space*self.spaceCount)+self.xml['subroutineDecb']+'\n')
		self.spaceCount += 1

		self.table.startSubroutine()

		if_param = False #ensures that at least an empty param list is discovered

		isConstruct = False

		while self.token.hasMoreTokens:
			tokentype = self.token.tokenType()

			if self.keyword in tokentype:
				tempkey = self.token.keyWord()

				if self.key_method in tempkey or self.key_function in tempkey or self.key_constructor in tempkey:
					self.of.write((self.space*self.spaceCount)+self.xml['keywordb']+tempkey.lower()+self.xml['keyworde']+'\n')
					isConstruct = True if self.key_constructor in tempkey else False

				elif self.key_int in tempkey or self.key_char in tempkey or self.key_boolean in tempkey or self.key_void in tempkey:
					self.of.write((self.space*self.spaceCount)+self.xml['keywordb']+tempkey.lower()+self.xml['keyworde']+'\n')

				#if the keyward var is in tempkey then we need to compile a vardeck
				elif self.key_var in tempkey:
					self.compileVarDec()

				#if it runs into any keywords that aren't caught by the above statements then it is no longer
				#in a subroutine
				else:
					break

			elif self.sym in tokentype:
				tempsym = self.token.symbol()

				#if it runs into a ( then it is descovering a parameter list
				if '(' in tempsym:
					self.of.write((self.space*self.spaceCount)+self.xml['symbolb']+tempsym+self.xml['symbole']+'\n')
					self.token.advance()
					#compiles the parameter list
					self.compileParameterList(isConstruct)

					self.of.write((self.space*self.spaceCount)+self.xml['subroutineBodyb']+'\n')
					self.of.write((self.space*self.spaceCount)+self.xml['symbolb']+self.token.symbol()+self.xml['symbole']+'\n')
					if_param = True #set param list discovered to true

				#if it has fond at lest an empty paramlist then it can print the next symboles 
				elif if_param:
					self.of.write((self.space*self.spaceCount)+self.xml['symbolb']+tempsym+self.xml['symbole']+'\n')

				#error
				else:
					print(self.token.errorMsg())
					sys.exit(0)

			elif self.ident in tokentype:
				self.of.write((self.space*self.spaceCount)+self.xml['identifierb']+self.token.identifier()+self.xml['identifiere']+'\n')

			self.token.advance()


		self.compileStatements()

		self.of.write((self.space*self.spaceCount)+self.xml['subroutineBodye']+'\n')

		self.spaceCount -= 1
		self.of.write((self.space*self.spaceCount)+self.xml['subroutineDece']+'\n')

	#------------------------------------------------------------------------------
	# This method compiles the parameter list
	def compileParameterList(self,isConstruct):
		self.of.write((self.space*self.spaceCount)+self.xml['parameterListb']+'\n')
		self.spaceCount += 1

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
				self.of.write((self.space*self.spaceCount)+self.xml['keywordb']+tempkey.lower()+self.xml['keyworde']+'\n')

			elif self.ident in tokentype:
				tempident = self.token.identifier()
				if len(curtype) == 0:
					curtype = tempident
				else:
					curname = tempident
				self.of.write((self.space*self.spaceCount)+self.xml['identifierb']+tempident+self.xml['identifiere']+'\n')

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
					self.of.write((self.space*self.spaceCount)+self.xml['symbolb']+tempsym+self.xml['symbole']+'\n')

				#any other symbol results in a an error
				else:
					print(self.token.errorMsg())
					sys.exit(0)
			
			self.token.advance()

		self.spaceCount -= 1
		self.of.write((self.space*self.spaceCount)+self.xml['parameterListe']+'\n')
		self.of.write((self.space*self.spaceCount)+self.xml['symbolb']+tempsym+self.xml['symbole']+'\n')
		
		#advance twice because we are at ( so need to getpast that and need to get the next symbol
		self.token.advance()
		self.token.advance()

	#------------------------------------------------------------------------------
	# This method compiles the var decliration
	def compileVarDec(self):
		self.of.write((self.space*self.spaceCount)+self.xml['varDecb']+'\n')
		self.spaceCount += 1

		curname = ''
		curtype = ''

		while self.token.hasMoreTokens():
			tokentype = self.token.tokenType()

			if self.keyword in tokentype:
				tempkey = self.token.keyWord()

				if self.key_var in tempkey:
					self.of.write((self.space*self.spaceCount)+self.xml['keywordb']+tempkey.lower()+self.xml['keyworde']+'\n')

				elif self.key_int in tempkey or self.key_char in tempkey or self.key_boolean in tempkey:
					curtype = tempkey
					self.of.write((self.space*self.spaceCount)+self.xml['keywordb']+tempkey.lower()+self.xml['keyworde']+'\n')

				#if any keyword is docovered than what is above then the vardec is over
				else:
					break

			elif self.ident in tokentype:
				tempident = self.token.identifier()
				if len(curtype) == 0:
					curtype = tempident
				else:
					curname = tempident
				self.of.write((self.space*self.spaceCount)+self.xml['identifierb']+tempident+self.xml['identifiere']+'\n')

			elif self.sym in tokentype:
				tempsym = self.token.symbol()

				if ',' in tempsym:
					self.table.Define(curname,curtype, 'VAR')
					curname = ''
					self.of.write((self.space*self.spaceCount)+self.xml['symbolb']+tempsym+self.xml['symbole']+'\n')

				#once ; is found then at the end of a vardec
				elif ';' in tempsym:
					self.table.Define(curname,curtype, 'VAR')
					self.of.write((self.space*self.spaceCount)+self.xml['symbolb']+tempsym+self.xml['symbole']+'\n')
					break

			self.token.advance()

		self.spaceCount -= 1
		self.of.write((self.space*self.spaceCount)+self.xml['varDece']+'\n')

	#------------------------------------------------------------------------------
	# This method compiles the statements
	def compileStatements(self):
		self.of.write((self.space*self.spaceCount)+self.xml['statementsb']+'\n')
		self.spaceCount += 1

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

		self.spaceCount -= 1
		self.of.write((self.space*self.spaceCount)+self.xml['statementse']+'\n')
		self.of.write((self.space*self.spaceCount)+self.xml['symbolb']+self.token.symbol()+self.xml['symbole']+'\n')

	#------------------------------------------------------------------------------
	# This method compiles the do 
	def compileDo(self):
		self.of.write((self.space*self.spaceCount)+self.xml['doStatementb']+'\n')
		self.spaceCount += 1

		while self.token.hasMoreTokens():
			tokentype = self.token.tokenType()

			if self.keyword in tokentype:
				tempkey = self.token.keyWord()

				if self.key_do in tempkey:
					self.of.write((self.space*self.spaceCount)+self.xml['keywordb']+tempkey.lower()+self.xml['keyworde']+'\n')

				#if any keyword other then do is discovered at this level it results in an error
				else:
					print(self.token.errorMsg())
					sys.exit(0)

			elif self.ident in tokentype:
				#compiles the expression with the value for a subroutine call passed in being true
				self.compileExpression(True)
				#once compileexpression is done then the current token is a ; signalling the end of a dostatment
				self.of.write((self.space*self.spaceCount)+self.xml['symbolb']+self.token.symbol()+self.xml['symbole']+'\n')
				self.token.advance()
				break

			self.token.advance()

		self.spaceCount -= 1
		self.of.write((self.space*self.spaceCount)+self.xml['doStatemente']+'\n')
		
	#------------------------------------------------------------------------------
	# This method compiles the letStatement
	def compileLet(self):
		self.of.write((self.space*self.spaceCount)+self.xml['letStatementb']+'\n')
		self.spaceCount += 1

		while self.token.hasMoreTokens():
			tokentype = self.token.tokenType()

			if self.keyword in tokentype:
				tempkey = self.token.keyWord()

				if self.key_let in tempkey:
					self.of.write((self.space*self.spaceCount)+self.xml['keywordb']+tempkey.lower()+self.xml['keyworde']+'\n')

				#if any other keyword is discovered it is an error
				else:
					print(self.token.errorMsg())
					sys.exit(0)

			elif self.ident in tokentype:
				tempident = self.token.identifier()
				self.of.write((self.space*self.spaceCount)+self.xml['identifierb']+'\n')
				self.of.write((self.space*(self.spaceCount+1))+'<name>'+tempident+'</name>'+'\n')
				self.of.write((self.space*(self.spaceCount+1))+'<type>'+self.table.typeOf(tempident)+'</type>'+'\n')
				self.of.write((self.space*(self.spaceCount+1))+'<kind>'+self.table.kindOf(tempident)+'</kind>'+'\n')
				self.of.write((self.space*(self.spaceCount+1))+'<index>'+repr(self.table.indexOf(tempident))+'</index>'+'\n')
				self.of.write((self.space*self.spaceCount)+self.xml['identifiere']+'\n')

			elif self.sym in tokentype:
				tempsym = self.token.symbol()
				#if [ is discovered it means that it is an array access
				if '[' in tempsym:
					self.of.write((self.space*self.spaceCount)+self.xml['symbolb']+tempsym+self.xml['symbole']+'\n')
					self.token.advance()
					self.compileExpression(False)
					self.of.write((self.space*self.spaceCount)+self.xml['symbolb']+self.token.symbol()+self.xml['symbole']+'\n')
					self.token.advance()
					#continue so that the bellow error catching isn't accidently triped hence the advance command
					#before this
					continue

				#this means that we compile th expression on the other side of the = sign
				elif '=' in tempsym:
					self.of.write((self.space*self.spaceCount)+self.xml['symbolb']+tempsym+self.xml['symbole']+'\n')
					self.token.advance()
					self.compileExpression(False)
					#sets tempsym to the current symbole
					tempsym = self.token.symbol()
				
				#if tempsym at this point is ; then end of let statement
				if ';' in self.token.symbol():
					self.of.write((self.space*self.spaceCount)+self.xml['symbolb']+tempsym+self.xml['symbole']+'\n')
					break

				#othre wise it is an error
				else:
					print(self.token.errorMsg())
					sys.exit(0)

			self.token.advance()

		self.spaceCount -= 1
		self.of.write((self.space*self.spaceCount)+self.xml['letStatemente']+'\n')

	#------------------------------------------------------------------------------
	# This method compiles the whileStatement
	def compileWhile(self):
		self.of.write((self.space*self.spaceCount)+self.xml['whileStatementb']+'\n')
		self.spaceCount += 1

		while self.token.hasMoreTokens():
			tokentype = self.token.tokenType()

			if self.keyword in tokentype:
				tempkey = self.token.keyWord()

				if self.key_while in tempkey:
					self.of.write((self.space*self.spaceCount)+self.xml['keywordb']+tempkey.lower()+self.xml['keyworde']+'\n')
				
				#if any other keyword is discovered at this level it is an error
				else:
					print(self.token.errorMsg())
					sys.exit(0)

			elif self.sym in tokentype:
				tempsym = self.token.symbol()

				#the condition of the while loop
				if '(' in tempsym:
					self.of.write((self.space*self.spaceCount)+self.xml['symbolb']+tempsym+self.xml['symbole']+'\n')
					self.token.advance()
					self.compileExpression(False)
					self.of.write((self.space*self.spaceCount)+self.xml['symbolb']+self.token.symbol()+self.xml['symbole']+'\n')

				#body of the while loop
				elif '{' in tempsym:
					self.of.write((self.space*self.spaceCount)+self.xml['symbolb']+tempsym+self.xml['symbole']+'\n')
					self.token.advance()
					self.compileStatements()
					#once the statments are compiled the whilestatment is done
					break

				#any other symbol at this level results in an error
				else:
					print(self.token.errorMsg())
					sys.exit(0)

			self.token.advance()

		self.spaceCount -= 1
		self.of.write((self.space*self.spaceCount)+self.xml['whileStatemente']+'\n')

	#------------------------------------------------------------------------------
	# This method compiles the ReturnStatement
	def compileReturn(self):
		self.of.write((self.space*self.spaceCount)+self.xml['ReturnStatementb']+'\n')
		self.spaceCount += 1

		while self.token.hasMoreTokens():
			tokentype = self.token.tokenType()

			if self.keyword in tokentype:
				tempkey = self.token.keyWord()

				if self.key_return in tempkey:
					self.of.write((self.space*self.spaceCount)+self.xml['keywordb']+tempkey.lower()+self.xml['keyworde']+'\n')

				#Any other keyword means that an exprssion is to be compiled and return is done
				else:
					self.compileExpression(False)
					self.of.write((self.space*self.spaceCount)+self.xml['symbolb']+self.token.symbol()+self.xml['symbole']+'\n')
					self.token.advance()
					break

			#other wise compile expression
			elif self.ident in tokentype or self.string_c in tokentype or self.intc in tokentype:
				self.compileExpression(False)
				self.of.write((self.space*self.spaceCount)+self.xml['symbolb']+self.token.symbol()+self.xml['symbole']+'\n')
				self.token.advance()
				break

			elif self.sym in tokentype:
				tempsym = self.token.symbol()

				#denotes the end of a return statment
				if ';' in tempsym:
					self.of.write((self.space*self.spaceCount)+self.xml['symbolb']+tempsym+self.xml['symbole']+'\n')
					break
				#any other symbol at this level is an error
				else:
					print(self.token.errorMsg())
					sys.exit(0)

			self.token.advance()

		self.spaceCount -= 1
		self.of.write((self.space*self.spaceCount)+self.xml['ReturnStatemente']+'\n')
		
	#------------------------------------------------------------------------------
	# This method compiles the ifStatement
	def compileIf(self):
		self.of.write((self.space*self.spaceCount)+self.xml['ifStatementb']+'\n')
		self.spaceCount += 1

		#this means that keyword if has been seen only once so if it seen again
		#that means it is a seperate if statment 
		seen_once = True

		while self.token.hasMoreTokens():
			tokentype = self.token.tokenType()

			if self.keyword in tokentype:
				tempkey = self.token.keyWord()

				if self.key_if in tempkey and seen_once:
					self.of.write((self.space*self.spaceCount)+self.xml['keywordb']+tempkey.lower()+self.xml['keyworde']+'\n')

				elif self.key_else in tempkey:
					self.of.write((self.space*self.spaceCount)+self.xml['keywordb']+tempkey.lower()+self.xml['keyworde']+'\n')

				#if any other keyword is seen then it is the end of an if statement
				else:
					break

			elif self.sym in tokentype:
				tempsym = self.token.symbol()

				#The condition of an if statment
				if '(' in tempsym:
					self.of.write((self.space*self.spaceCount)+self.xml['symbolb']+tempsym+self.xml['symbole']+'\n')
					self.token.advance()
					self.compileExpression(False)
					self.of.write((self.space*self.spaceCount)+self.xml['symbolb']+self.token.symbol()+self.xml['symbole']+'\n')

				#body of an if|else statment
				elif '{' in tempsym:
					self.of.write((self.space*self.spaceCount)+self.xml['symbolb']+tempsym+self.xml['symbole']+'\n')
					self.token.advance()
					self.compileStatements()
					seen_once = False

			self.token.advance()

		self.spaceCount -= 1
		self.of.write((self.space*self.spaceCount)+self.xml['ifStatemente']+'\n')

	#------------------------------------------------------------------------------
	# This method compiles the expression
	def compileExpression(self,subCall):
		#if it a subrountine call don't want to print out the exprssion attribute
		if not subCall:
			self.of.write((self.space*self.spaceCount)+self.xml['expressionb']+'\n')

		self.spaceCount += 1

		while self.token.hasMoreTokens():
			tokentype = self.token.tokenType()

			if self.sym in tokentype:
				tempsym = self.token.symbol()

				#if it is an operator then print out the appropriate xml attribute statement
				if tempsym in '+-*/&|<>=':
					if '<' in tempsym:
						self.of.write((self.space*self.spaceCount)+self.xml['symbolb']+"&lt;"+self.xml['symbole']+'\n')

					elif '>' in tempsym:
						self.of.write((self.space*self.spaceCount)+self.xml['symbolb']+"&gt;"+self.xml['symbole']+'\n')

					elif '&' in tempsym:
						self.of.write((self.space*self.spaceCount)+self.xml['symbolb']+"&amp;"+self.xml['symbole']+'\n')

					else:
						self.of.write((self.space*self.spaceCount)+self.xml['symbolb']+tempsym+self.xml['symbole']+'\n')

				#this means that we have term to compile
				elif tempsym in '(~':
					self.compileTerm(subCall)

				#signifies the end of an expression
				elif tempsym in ';)],':
					break

			else:
				self.compileTerm(subCall)

			self.token.advance()

		self.spaceCount -= 1
		if not subCall:
			self.of.write((self.space*self.spaceCount)+self.xml['expressione']+'\n')

	#------------------------------------------------------------------------------
	# This method compiles the term
	def compileTerm(self,subCall):
		if not subCall:
			self.of.write((self.space*self.spaceCount)+self.xml['termb']+'\n')

		self.spaceCount += 1

		while self.token.hasMoreTokens():
			tokentype = self.token.tokenType()

			if self.keyword in tokentype:
				tempkey = self.token.keyWord()

				if self.key_true in tempkey or self.key_false in tempkey or self.key_null in tempkey or self.key_this in tempkey:
					self.of.write((self.space*self.spaceCount)+self.xml['keywordb']+tempkey.lower()+self.xml['keyworde']+'\n')
				
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
					#replace this with code to do a look up
					self.of.write((self.space*self.spaceCount)+self.xml['identifierb']+'\n')
					self.of.write((self.space*(self.spaceCount+1))+'<name>'+tempident+'</name>'+'\n')
					self.of.write((self.space*(self.spaceCount+1))+'<type>'+self.table.typeOf(tempident)+'</type>'+'\n')
					self.of.write((self.space*(self.spaceCount+1))+'<kind>'+self.table.kindOf(tempident)+'</kind>'+'\n')
					self.of.write((self.space*(self.spaceCount+1))+'<index>'+repr(self.table.indexOf(tempident))+'</index>'+'\n')
					self.of.write((self.space*self.spaceCount)+self.xml['identifiere']+'\n')

					self.token.advance()

					tempsym = self.token.symbol()
					self.of.write((self.space*self.spaceCount)+self.xml['symbolb']+tempsym+self.xml['symbole']+'\n')
					self.token.advance()

					tempident = self.token.identifier()
					self.of.write((self.space*self.spaceCount)+self.xml['identifierb']+tempident+self.xml['identifiere']+'\n')
					self.token.advance()

					tempsym = self.token.symbol()
					self.of.write((self.space*self.spaceCount)+self.xml['symbolb']+tempsym+self.xml['symbole']+'\n')
					self.token.advance()

					#then compiles the expression list
					self.compileExpressionList()

				#this means that it is a subroutine call to one of its own methods
				elif '(' in peaks:

					self.of.write((self.space*self.spaceCount)+self.xml['identifierb']+tempident+self.xml['identifiere']+'\n')
					self.token.advance()
					
					tempsym = self.token.symbol()
					self.of.write((self.space*self.spaceCount)+self.xml['symbolb']+tempsym+self.xml['symbole']+'\n')
					self.token.advance()

					self.compileExpressionList()

				#this means that it is accessing an array element
				elif '[' in peaks:
					self.of.write((self.space*self.spaceCount)+self.xml['identifierb']+'\n')
					self.of.write((self.space*(self.spaceCount+1))+'<name>'+tempident+'</name>'+'\n')
					self.of.write((self.space*(self.spaceCount+1))+'<type>'+self.table.typeOf(tempident)+'</type>'+'\n')
					self.of.write((self.space*(self.spaceCount+1))+'<kind>'+self.table.kindOf(tempident)+'</kind>'+'\n')
					self.of.write((self.space*(self.spaceCount+1))+'<index>'+repr(self.table.indexOf(tempident))+'</index>'+'\n')
					self.of.write((self.space*self.spaceCount)+self.xml['identifiere']+'\n')
					self.token.advance()
					
					tempsym = self.token.symbol()
					self.of.write((self.space*self.spaceCount)+self.xml['symbolb']+tempsym+self.xml['symbole']+'\n')
					self.token.advance()

					self.compileExpression(subCall)

					tempsym = self.token.symbol()
					self.of.write((self.space*self.spaceCount)+self.xml['symbolb']+tempsym+self.xml['symbole']+'\n')

				#other wise it is just an identifier
				else:
					self.of.write((self.space*self.spaceCount)+self.xml['identifierb']+'\n')
					self.of.write((self.space*(self.spaceCount+1))+'<name>'+tempident+'</name>'+'\n')
					self.of.write((self.space*(self.spaceCount+1))+'<type>'+self.table.typeOf(tempident)+'</type>'+'\n')
					self.of.write((self.space*(self.spaceCount+1))+'<kind>'+self.table.kindOf(tempident)+'</kind>'+'\n')
					self.of.write((self.space*(self.spaceCount+1))+'<index>'+repr(self.table.indexOf(tempident))+'</index>'+'\n')
					self.of.write((self.space*self.spaceCount)+self.xml['identifiere']+'\n')

			elif self.intc in tokentype:
				self.of.write((self.space*self.spaceCount)+self.xml['integerConstantb']+self.token.intVal()+self.xml['integerConstante']+'\n')

			elif self.string_c in tokentype:
				self.of.write((self.space*self.spaceCount)+self.xml['StringConstantb']+self.token.stringVal()+self.xml['StringConstante']+'\n')

			elif self.sym in tokentype:
				tempsym = self.token.symbol()

				#this means that it is and expression surrounded by ()
				if '(' in tempsym:
					self.of.write((self.space*self.spaceCount)+self.xml['symbolb']+tempsym+self.xml['symbole']+'\n')
					self.token.advance()
					self.compileExpression(subCall)

					tempsym = self.token.symbol()
					self.of.write((self.space*self.spaceCount)+self.xml['symbolb']+tempsym+self.xml['symbole']+'\n')

				#not unary operator 
				elif '~' in tempsym:
					self.of.write((self.space*self.spaceCount)+self.xml['symbolb']+tempsym+self.xml['symbole']+'\n')
					self.token.advance()
					self.compileTerm(subCall)

				#operator
				elif tempsym in '+-*/&|<>=':
					self.spaceCount -= 1
					self.of.write((self.space*self.spaceCount)+self.xml['terme']+'\n')
					if '<' in tempsym:
						self.of.write((self.space*self.spaceCount)+self.xml['symbolb']+"&lt;"+self.xml['symbole']+'\n')

					elif '>' in tempsym:
						self.of.write((self.space*self.spaceCount)+self.xml['symbolb']+"&gt;"+self.xml['symbole']+'\n')

					elif '&' in tempsym:
						self.of.write((self.space*self.spaceCount)+self.xml['symbolb']+"&amp;"+self.xml['symbole']+'\n')

					else:
						self.of.write((self.space*self.spaceCount)+self.xml['symbolb']+tempsym+self.xml['symbole']+'\n')

					return
					
			#if the next token is ]);, means the end of a term
			if self.token.peak() in ']);,':
				break

			self.token.advance()

		self.spaceCount -= 1
		if not subCall:
			self.of.write((self.space*self.spaceCount)+self.xml['terme']+'\n')

	#------------------------------------------------------------------------------
	# This method compiles the expressionList
	def compileExpressionList(self):
		self.of.write((self.space*self.spaceCount)+self.xml['expressionListb']+'\n')
		self.spaceCount += 1

		while self.token.hasMoreTokens():
			tokentype = self.token.tokenType()

			if self.sym in tokentype:
				tempsym = self.token.symbol()

				#indicates teh start of another expression
				if ',' in tempsym:
					self.of.write((self.space*self.spaceCount)+self.xml['symbolb']+tempsym+self.xml['symbole']+'\n')
					self.token.advance()
					self.compileExpression(False)

				#indicates that end of expression list
				elif ')' in tempsym:
					break
				#other wise compile expression
				else:
					self.compileExpression(False)
			else:
				self.compileExpression(False)

		self.spaceCount -= 1
		self.of.write((self.space*self.spaceCount)+self.xml['expressionListe']+'\n')
		self.of.write((self.space*self.spaceCount)+self.xml['symbolb']+self.token.symbol()+self.xml['symbole']+'\n')

#-------------------End Class--------------------------------------------------