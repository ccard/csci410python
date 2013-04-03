import sys, string, os, io,re
from jacktokenizer import JackToken
#------------------------------------------------------------------------------
#Chris Card
#CS410
#ECS project 10
#python 3.3
#Due:3/25/13
#This is the main of the program run this
#------------------------------------------------------------------------------

class CompilationEngine:
	#------------------------------------------------------------------------------
	# Var Declar:
	#------------------------------------------------------------------------------
	
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
	
	keyword='KEYWORD'
	sym='SYMBOL'
	ident='IDENTIFIER'
	intc='INT_CONST'
	string_c='STRING_CONST'
	space = ' '
	spaceCount = 0
	
	xml={'classb':'<class>','classe':'</class>','classVarDecb':'<classVarDec>','classVarDece':'</classVarDec>','typeb':'<type>','typee':'</type>'
		,'subroutineDecb':'<subroutineDec>','subroutineDece':'</subroutineDec>','parameterListb':'<parameterList>','parameterListe':'</parameterList>'
		,'subroutineBodyb':'<subroutineBody>','subroutineBodye':'</subroutineBody>','varDecb':'<varDec>','varDece':'</varDec>','classNameb':'<className>'
		,'classNamee':'</className>','subrountineNameb':'<subrountineName>','subrountineNamee':'</subrountineName>','varNameb':'<varName>','varNamee':'</varName>'
		,'statementsb':'<statements>','statementse':'</statements>','letStatementb':'<letStatement>','letStatemente':'</letStatement>'
		,'ifStatementb':'<ifStatement>','ifStatemente':'</ifStatement>','whileStatementb':'<whileStatement>','whileStatemente':'</whileStatement>'
		,'doStatementb':'<doStatement>','doStatemente':'</doStatement>','ReturnStatementb':'<ReturnStatement>','ReturnStatemente':'</ReturnStatement>'
		,'expressionb':'<expression>','expressione':'</expression>','termb':'<term>','terme':'</term>','subroutineCallb':'<subroutineCall>'
		,'subroutineCalle':'</subroutineCall>','expressionListb':'<expressionList>','expressionListe':'</expressionList>','opb':'<op>','ope':'</op>'
		,'unaryOPb':'<unaryOP>','unaryOPe':'</unaryOP>','KeywrodConstantb':'<KeywrodConstant>','KeywrodConstante':'</KeywrodConstant>'
		,'integerConstantb':'<integerConstant>','integerConstante':'</integerConstant>','StringConstantb':'<StringConstant>','StringConstante':'</StringConstant>'
		,'identifierb':'<identifier>','identifiere':'</identifier>','keywordb':'<keyword>','keyworde':'</keyword>',
		'symbolb':'<symbol>', 'symbole':'</symbol>'}
	
	
	#------------------------------------------------------------------------------
	# This is the constructor
	def __init__(self,infile,outfile):
		self.of = open(outfile,'w')
		self.token = JackToken(infile)
	
	#------------------------------------------------------------------------------
	# This method compiles the class
	def compileClass(self):
		self.of.write((self.space*self.spaceCount)+self.xml['classb'])
		self.spaceCount += 1
		self.token.advance()
		while self.token.hasMoreTokens():
			tokentype = self.token.tokenType()
			if self.keyword in tokentype:
				tempkey = self.token.keyWord()
				if self.key_class in tempkey:
					self.of.write((self.space*self.spaceCount)+self.xml['keywordb']+tempkey.lower()+self.xml['keyworde'])
				
				elif self.key_static in tempkey or self.key_field in tempkey:
					self.compileClassVarDec()

				elif self.key_constructor in tempkey or self.key_method in tempkey or self.key_function in tempkey:
					self.compileSubroutine()

			elif self.sym in tokentype:
				tempsym = self.token.symbol()
				self.of.write((self.space*self.spaceCount)+self.xml['symbolb']+tempsym+self.xml['symbole'])

			elif self.ident in tokentype:
				tempident = self.token.identifier()
				self.of.write((self.space*self.spaceCount)+self.xml['identifierb']+tempident+self.xml['identifiere'])
			self.token.advance()

	#------------------------------------------------------------------------------
	# This method compiles class var dec
	def compileClassVarDec(self):
		self.of.write((self.space*self.spaceCount)+self.xml['classVarDecb'])
		self.spaceCount += 1

		ifSemiCol = False

		while self.token.hasMoreTokens:
			tokentype = self.token.tokenType()
			if self.keyword in tokentype:
				tempkey = self.token.keyWord()
				if self.key_int in tempkey or self.key_char in tempkey or self.key_boolean in tempkey and not ifSemiCol:
					self.of.write((self.space*self.spaceCount)+self.xml['typeb']+tempkey.lower()+self.xml['typee'])

				elif self.key_static in tempkey or self.key_field in tempkey and ifSemiCol:
					self.of.write((self.space*self.spaceCount)+self.xml['keywordb']+tempkey.lower()+self.xml['keyworde'])

				else:
					break

				ifSemiCol = False
					
			elif self.identifier in tokentype:
				tempident = self.token.identifier()
				self.of.write((self.space*self.spaceCount)+self.xml['identifierb']+tempident+self.xml['identifiere'])

			elif self.sym in tokentype:
				tempsym = self.token.symbol()
				if ',' in tempsym and ifSemiCol:
					print("ERROR: syntax violation a ',' came after ';'\n")
					sys.exit(0)
				if re.search('[\(\)\{\}\[\]\.\+\-\*\/\&\<\>\=\~]{1}',tempsym) is not None:
					print("ERROR: syntax violation a invalid symbol occured in var decliration section\n")
					sys.exit(0)

				if ';' in tempsym:
					ifSemiCol = True
				self.of.write((self.space*self.spaceCount)+self.xml['symbolb']+tempident+self.xml['symbole'])

			self.token.advance()

		self.spaceCount -= 1
		self.of.write((self.space*self.spaceCount)+self.xml['classVarDece'])

	#------------------------------------------------------------------------------
	# This method compiles the subroutines
	def compileSubroutine(self):
		self.of.write((self.space*self.spaceCount)+self.xml['subroutineDecb'])
		self.spaceCount += 1

		while self.token.hasMoreTokens:
			tokentype = self.token.tokenType()
			if self.keyword in tokentype:
				tempkey = self.token.keyWord()
				if self.key_method in tempkey or self.key_function in tempkey or self.key_constructor in tempkey:
					self.of.write((self.space*self.spaceCount)+self.xml['keywordb']+tempkey.lower()+self.xml['keyworde'])

				elif self.key_int in tempkey or self.key_char in tempkey or self.key_boolean in tempkey or self.key_void in tempkey:
					self.of.write((self.space*self.spaceCount)+self.xml['typeb']+tempkey.lower()+self.xml['typee'])

			elif self.sym in tokentype:
				tempsym = self.token.symbol()
				if '(' in tempsym:
					self.of.write((self.space*self.spaceCount)+self.xml['symbolb']+tempsym+self.xml['symbole'])
					self.token.advance()
					self.compileParameterList()
					self.of.write((self.space*self.spaceCount)+self.xml['subroutineBodyb'])
					break
				else:
					self.of.write((self.space*self.spaceCount)+self.xml['symbolb']+tempsym+self.xml['symbole'])

			elif self.ident in tokentype:
				self.of.write((self.space*self.spaceCount)+self.xml['identifierb']+self.token.identifier()+self.xml['identifiere'])

			self.token.advance()

		self.compileVarDec()

		self.compileStatements()

		self.of.write((self.space*self.spaceCount)+self.xml['subroutineBodye'])

		self.spaceCount -= 1
		self.of.write((self.space*self.spaceCount)+self.xml['subroutineDece'])

	#------------------------------------------------------------------------------
	# This method compiles the parameter list
	def compileParameterList(self):
		self.of.write((self.space*self.spaceCount)+self.xml['parameterListb'])
		self.spaceCount += 1

		while self.token.hasMoreTokens():
			tokentype = self.token.tokenType()

			if self.keyword in tokentype:
				tempkey = self.token.keyWord()
				self.of.write((self.space*self.spaceCount)+self.xml['typeb']+tempkey.lower()+self.xml['typee'])

			elif self.ident in tokentype:
				tempident = self.token.identifier()
				self.of.write((self.space*self.spaceCount)+self.xml['identifierb']+tempident+self.xml['identifiere'])

			elif self.sym in tokentype:
				tempsym = self.token.symbol()
				if ')' in tempsym:
					self.of.write((self.space*self.spaceCount)+self.xml['symbolb']+tempsym+self.xml['symbole'])
					self.token.advance()
					break

				elif ',' in tempsym:
					self.of.write((self.space*self.spaceCount)+self.xml['symbolb']+tempsym+self.xml['symbole'])

				else:
					print("ERROR: syntax violation in parameterlsit\n")
					sys.exit(0)
			
			self.token.advance()

		self.spaceCount -= 1
		self.of.write((self.space*self.spaceCount)+self.xml['parameterListe'])
		sys.token.advance()

	#------------------------------------------------------------------------------
	# This method compiles the var decliration
	def compileVarDec(self):
		self.of.write((self.space*self.spaceCount)+self.xml['varDecb'])
		self.spaceCount += 1

		while self.token.hasMoreTokens():
			tokentype = self.token.tokenType()

			if self.keyword in tokentype:
				tempkey = self.token.keyWord()
				if self.key_var in tempkey:
					self.of.write((self.space*self.spaceCount)+self.xml['keywordb']+tempkey.lower()+self.xml['keyworde'])

				elif or self.key_int in tempkey or self.key_char in tempkey or self.key_boolean in tempkey:
					self.of.write((self.space*self.spaceCount)+self.xml['typeb']+tempkey.lower()+self.xml['typee'])

				else:
					break

			elif self.ident in tokentype:
				tempident = self.token.identifier()
				self.of.write((self.space*self.spaceCount)+self.xml['identifierb']+tempident+self.xml['identifiere'])

			elif self.sym in tokentype:
				tempsym = self.token.symbol()
				self.of.write((self.space*self.spaceCount)+self.xml['symbolb']+tempsym+self.xml['symbole'])

			self.token.advance()

		self.spaceCount -= 1
		self.of.write((self.space*self.spaceCount)+self.xml['varDece'])

	#------------------------------------------------------------------------------
	# This method compiles the statements
	def compileStatements(self):
		self.of.write((self.space*self.spaceCount)+self.xml['statementsb'])
		self.spaceCount += 1

		while self.token.hasMoreTokens():
			tokentype = self.token.tokenType()

			if self.keyword in tokentype:
				tempkey = self.token.keyWord()
				if self.key_let in tempkey:
					self.compileLet()

				elif self.key_if in tempkey:
					self.compileIf()

				elif self.key_while in tempkey:
					self.compileWhile()

				elif self.key_do in tempkey:
					self.compileDo()

				elif self.key_return in tempkey:
					self.compileReturn()

				else:
					print("ERROR: syntax violation for statments of a subroutine")
					sys.exit(0)
			elif self.sym in tokentype:
				tempsym = self.token.symbol()
				if '}' in tempsym:
					break
				else:
					print("ERROR: syntax violation for statments of a subroutine")
					sys.exit(0)

			self.token.advance()

		self.spaceCount -= 1
		self.of.write((self.space*self.spaceCount)+self.xml['statementse'])
		self.of.write((self.space*self.spaceCount)+self.xml['symbolb']+self.token.symbol()+self.xml['symbole'])

	#------------------------------------------------------------------------------
	# This method compiles the do 
	def compileDo(self):
		self.of.write((self.space*self.spaceCount)+self.xml['doStatementb'])
		self.spaceCount += 1
		subCallb = True

		while self.token.hasMoreTokens():
			tokentype = self.token.tokenType()
			if self.keyword in tokentype:
				tempkey = self.keyWord()
				if self.key_do in tempkey:
					self.of.write((self.space*self.spaceCount)+self.xml['keywordb']+tempkey.lower()+self.xml['keyworde'])
				else:
					print("ERROR: syntax violation")
					sys.exit(0)

			elif self.ident in tokentype:
				self.compileExpression()
				self.of.write((self.space*self.spaceCount)+self.xml['symbolb']+self.token.symbol()+self.xml['symbole'])
				self.token.advance()
				break

			self.token.advance()

		self.spaceCount -= 1
		self.of.write((self.space*self.spaceCount)+self.xml['doStatemente'])
		
	#------------------------------------------------------------------------------
	# This method compiles the letStatement
	def compileLet(self):
		self.of.write((self.space*self.spaceCount)+self.xml['letStatementb'])
		self.spaceCount += 1

		while self.token.hasMoreTokens():
			tokentype = self.token.tokenType()
			if self.keyword in tokentype:
				tempkey = self.token.keyWord()
				if self.key_let in tempkey:
					self.of.write((self.space*self.spaceCount)+self.xml['keywordb']+tempkey.lower()+self.xml['keyworde'])
				else:
					print("ERROR: syntax violation")
					sys.exit(0)

			elif self.ident in tokentype:
				tempident = self.token.identifier()
				self.of.write((self.space*self.spaceCount)+self.xml['identifierb']+tempident+self.xml['identifiere'])

			elif self.sym in tokentype:
				tempsym = self.token.symbol()
				if '[' in tempsym:
					self.of.write((self.space*self.spaceCount)+self.xml['symbolb']+tempsym+self.xml['symbole'])
					self.token.advance()
					self.compileExpression()
					self.of.write((self.space*self.spaceCount)+self.xml['symbolb']+self.token.symbol()+self.xml['symbole'])
				elif '=' in tempsym:
					self.of.write((self.space*self.spaceCount)+self.xml['symbolb']+tempsym+self.xml['symbole'])
					self.token.advance()
					self.compileExpression()
					self.of.write((self.space*self.spaceCount)+self.xml['symbolb']+self.token.symbol()+self.xml['symbole'])
				
				if ';' in self.token.symbol():
					self.of.write((self.space*self.spaceCount)+self.xml['symbolb']+tempsym+self.xml['symbole'])
					break
				else:
					print("ERROR: syntax violation")

			self.token.advance()

		self.spaceCount -= 1
		self.of.write((self.space*self.spaceCount)+self.xml['letStatemente'])

	#------------------------------------------------------------------------------
	# This method compiles the whileStatement
	def compileWhile(self):
		self.of.write((self.space*self.spaceCount)+self.xml['whileStatementb'])
		self.spaceCount += 1

		while self.token.hasMoreTokens():
			tokentype = self.token.tokenType()
			if self.keyword in tokentype:
				tempkey = self.token.keyWord()
				if self.key_while in tempkey:
					self.of.write((self.space*self.spaceCount)+self.xml['keywordb']+tempkey.lower()+self.xml['keyworde'])
				else:
					print("ERROR: syntax violation")
					sys.exit(0)

			elif self.sym in tokentype:
				tempsym = self.token.symbol()
				if '(' in tempsym:
					self.of.write((self.space*self.spaceCount)+self.xml['symbolb']+tempsym+self.xml['symbole'])
					self.token.advance()
					self.compileExpression()
					self.of.write((self.space*self.spaceCount)+self.xml['symbolb']+self.token.symbol()+self.xml['symbole'])
				elif '{' in tempsym:
					self.of.write((self.space*self.spaceCount)+self.xml['symbolb']+tempsym+self.xml['symbole'])
					self.token.advance()
					self.compileStatements()
					break
				else:
					print("ERROR: syntax violation")
					sys.exit(0)

			self.token.advance()

		self.spaceCount -= 1
		self.of.write((self.space*self.spaceCount)+self.xml['whileStatemente'])

	#------------------------------------------------------------------------------
	# This method compiles the ReturnStatement
	def compileReturn(self):
		self.of.write((self.space*self.spaceCount)+self.xml['ReturnStatementb'])
		self.spaceCount += 1

		while self.token.hasMoreTokens():
			tokentype = self.token.tokenType()
			if self.keyword in tokentype:
				tempkey = self.token.keyWord()
				if self.key_return in tempkey:
					self.of.write((self.space*self.spaceCount)+self.xml['keywordb']+tempkey.lower()+self.xml['keyworde'])

				else:
					self.compileExpression()

			elif self.ident in tokentype or self.string_c in tokentype or self.intc in tokentype:
				self.compileExpression()

			elif self.sym in tokentype:
				tempsym = self.token.symbol()
				if ';' in tempsym:
					self.of.write((self.space*self.spaceCount)+self.xml['symbolb']+tempsym+self.xml['symbole'])
					break
				else:
					print("ERROR: syntax violation")

			self.token.advance()

		self.spaceCount += 1
		self.of.write((self.space*self.spaceCount)+self.xml['ReturnStatemente'])
		
	#------------------------------------------------------------------------------
	# This method compiles the ifStatement
	def compileIf(self):
		self.of.write((self.space*self.spaceCount)+self.xml['ifStatementb'])
		self.spaceCount += 1

		while self.token.hasMoreTokens():
			tokentype = self.token.tokenType()
			if self.keyword in tokentype:
				tempkey = self.token.keyWord()
				if self.key_if in tempkey:
					self.of.write((self.space*self.spaceCount)+self.xml['keywordb']+tempkey.lower()+self.xml['keyworde'])

				elif self.key_else in tempkey:
					self.of.write((self.space*self.spaceCount)+self.xml['keywordb']+tempkey.lower()+self.xml['keyworde'])

				else:
					break

			elif self.sym in tokentype:
				tempsym = self.token.symbol
				if '(' in tempsym:
					self.of.write((self.space*self.spaceCount)+self.xml['symbolb']+tempsym+self.xml['symbole'])
					self.token.advance()
					self.compileExpression()

				elif '{' in tempsym:
					self.of.write((self.space*self.spaceCount)+self.xml['symbolb']+tempsym+self.xml['symbole'])
					self.token.advance()
					self.compileStatements()

			self.token.advance()

		self.spaceCount += 1
		self.of.write((self.space*self.spaceCount)+self.xml['ifStatemente'])

	#------------------------------------------------------------------------------
	# This method compiles the expression
	def compileExpression(self):
		self.of.write((self.space*self.spaceCount)+self.xml['expressionb'])
		self.spaceCount += 1

		while self.token.hasMoreTokens():
			tokentype = self.token.tokenType()
			if self.sym in tokentype:
				tempsym = self.token.symbol()
				if tempsym in '+-*/&|<>=':
					self.of.write((self.space*self.spaceCount)+self.xml['opb']+tempsym+self.xml['ope'])
				elif tempsym in ';)],':
					break
			else:
				self.compileTerm()

			self.token.advance()

		self.spaceCount -= 1
		self.of.write((self.space*self.spaceCount)+self.xml['expressione'])

	#------------------------------------------------------------------------------
	# This method compiles the term
	def compileTerm(self):
		self.of.write((self.space*self.spaceCount)+self.xml['termb'])
		self.spaceCount += 1

		while self.token.hasMoreTokens():
			tokentype = self.token.tokenType()
			if self.keyword in tokentype:
				tempkey = self.token.keyWord()
				if self.key_true in tempkey or self.key_false in tempkey or self.key_null in tempkey or self.key_this in tempkey:
					self.of.write((self.space*self.spaceCount)+self.xml['KeywrodConstantb']+tempkey.lower()+self.xml['KeywrodConstante'])
				
				else:
					print("ERROR: syntax violation")
					sys.exit(0)

			elif self.ident in tokentype:
				tempident = self.token.identifier()
				peaks = self.token.peak()
				if '.' in peaks:
					self.of.write((self.space*self.spaceCount)+self.xml['subroutineCallb'])
					self.spaceCount += 1

					#replace this with code to do a look up
					self.of.write((self.space*self.spaceCount)+self.xml['identifierb']+tempident+self.xml['identifiere'])
					self.token.advance()

					tempsym = self.token.symbol()
					self.of.write((self.space*self.spaceCount)+self.xml['symbolb']+tempsym+self.xml['symbole'])
					self.token.advance()

					tempident = self.token.identifier()
					self.of.write((self.space*self.spaceCount)+self.xml['identifierb']+tempident+self.xml['identifiere'])
					self.token.advance()

					tempsym = self.token.symbol()
					self.of.write((self.space*self.spaceCount)+self.xml['symbolb']+tempsym+self.xml['symbole'])
					self.token.advance()

					self.compileExpressionList()
					self.spaceCount -= 1
					self.of.write((self.space*self.spaceCount)+self.xml['subroutineCalle'])

				elif '(' in peaks:
					self.of.write((self.space*self.spaceCount)+self.xml['subroutineCallb'])
					self.spaceCount += 1

					self.of.write((self.space*self.spaceCount)+self.xml['identifierb']+tempident+self.xml['identifiere'])
					self.token.advance()
					
					tempsym = self.token.symbol()
					self.of.write((self.space*self.spaceCount)+self.xml['symbolb']+tempsym+self.xml['symbole'])
					self.token.advance()

					self.compileExpressionList()

					self.spaceCount -= 1
					self.of.write((self.space*self.spaceCount)+self.xml['subroutineCalle'])

				elif '[' in peaks:
					self.of.write((self.space*self.spaceCount)+self.xml['identifierb']+tempident+self.xml['identifiere'])
					self.token.advance()
					
					tempsym = self.token.symbol()
					self.of.write((self.space*self.spaceCount)+self.xml['symbolb']+tempsym+self.xml['symbole'])
					self.token.advance()

					self.compileExpression()

					tempsym = self.token.symbol()
					self.of.write((self.space*self.spaceCount)+self.xml['symbolb']+tempsym+self.xml['symbole'])

			elif self.intc in tokentype:
				self.of.write((self.space*self.spaceCount)+self.xml['integerConstantb']+self.token.intVal()+self.xml['integerConstante'])

			elif self.string_c in tokentype:
				self.of.write((self.space*self.spaceCount)+self.xml['StringConstantb']+self.token.stringVal()+self.xml['StringConstante'])

			elif self.sym in tokentype:
				tempsym = self.token.symbol()
				if '(' in tempsym:
					self.of.write((self.space*self.spaceCount)+self.xml['symbolb']+tempsym+self.xml['symbole'])
					self.token.advance()
					self.compileExpression()

					tempsym = self.token.symbol()
					self.of.write((self.space*self.spaceCount)+self.xml['symbolb']+tempsym+self.xml['symbole'])

				elif tempsym in '-~':
					self.of.write((self.space*self.spaceCount)+self.xml['unaryOPb']+tempsym+self.xml['unaryOPe'])
					self.token.advance()
					self.compileTerm()

			if self.token.peak() in ']);,':
				break

			self.token.advance()

		self.spaceCount -= 1
		self.of.write((self.space*self.spaceCount)+self.xml['terme'])

	#------------------------------------------------------------------------------
	# This method compiles the expressionList
	def compileExpressionList(self):
		self.of.write((self.space*self.spaceCount)+self.xml['expressionListb'])
		self.spaceCount += 1

		while self.token.hasMoreTokens():
			tokentype = self.token.tokenType()

			if self.sym in tokentype:
				tempsym = self.token.symbol()
				if ',' in tempsym:
					self.of.write((self.space*self.spaceCount)+self.xml['symbolb']+tempsym+self.xml['symbole'])
					self.token.advance()
					self.compileExpression()
				elif ')' in tempsym:
					break
				else:
					print("ERROR: syntax violation")
					sys.exit(0)
			else:

		self.spaceCount -= 1
		self.of.write((self.space*self.spaceCount)+self.xml['expressionListe'])
		self.of.write((self.space*self.spaceCount)+self.xml['symbolb']+self.token.symbol()+self.xml['symbole'])
