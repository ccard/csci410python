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
	
	
	#------------------------------------------------------------------------------
	# This is the constructor
	def __init__(self,infile,outfile):
		self.of = open(outfile,'w')
		self.token = JackToken(infile)
	
	#------------------------------------------------------------------------------
	# This method compiles the class
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
				
				elif self.key_static in tempkey or self.key_field in tempkey:
					self.compileClassVarDec()
					continue

				elif self.key_constructor in tempkey or self.key_method in tempkey or self.key_function in tempkey:
					self.compileSubroutine()

			elif self.sym in tokentype:
				tempsym = self.token.symbol()
				if '}' in tempsym:
					self.of.write((self.space*self.spaceCount)+self.xml['symbolb']+tempsym+self.xml['symbole']+'\n')
					break
				self.of.write((self.space*self.spaceCount)+self.xml['symbolb']+tempsym+self.xml['symbole']+'\n')

			elif self.ident in tokentype:
				tempident = self.token.identifier()
				self.of.write((self.space*self.spaceCount)+self.xml['identifierb']+tempident+self.xml['identifiere']+'\n')

			self.token.advance()

		self.spaceCount -= 1
		self.of.write((self.space*self.spaceCount)+self.xml['classe'])

	#------------------------------------------------------------------------------
	# This method compiles class var dec
	def compileClassVarDec(self):
		self.of.write((self.space*self.spaceCount)+self.xml['classVarDecb']+'\n')
		self.spaceCount += 1

		ifSemiCol = False

		while self.token.hasMoreTokens:
			tokentype = self.token.tokenType()
			if self.keyword in tokentype:
				tempkey = self.token.keyWord()
				if self.key_int in tempkey or self.key_char in tempkey or self.key_boolean in tempkey:
					self.of.write((self.space*self.spaceCount)+self.xml['keywordb']+tempkey.lower()+self.xml['keyworde']+'\n')

				elif self.key_static in tempkey or self.key_field in tempkey:
					self.of.write((self.space*self.spaceCount)+self.xml['keywordb']+tempkey.lower()+self.xml['keyworde']+'\n')

				elif self.key_function in tempkey or self.key_method in tempkey or self.key_constructor in tempkey:
					break
					
			elif self.ident in tokentype:
				tempident = self.token.identifier()
				self.of.write((self.space*self.spaceCount)+self.xml['identifierb']+tempident+self.xml['identifiere']+'\n')

			elif self.sym in tokentype:
				tempsym = self.token.symbol()
				if ',' in tempsym and ifSemiCol:
					print("ERROR: syntax violation a ',' came after ';'\n")
					sys.exit(0)
				if re.search('[\(\)\{\}\[\]\.\+\-\*\/\&\<\>\=\~]{1}',tempsym) is not None:
					print(self.token.errorMsg())
					sys.exit(0)

				if ';' in tempsym:
					self.of.write((self.space*self.spaceCount)+self.xml['symbolb']+tempsym+self.xml['symbole']+'\n')
					self.token.advance()
					break

				self.of.write((self.space*self.spaceCount)+self.xml['symbolb']+tempsym+self.xml['symbole']+'\n')

			self.token.advance()

		self.spaceCount -= 1
		self.of.write((self.space*self.spaceCount)+self.xml['classVarDece']+'\n')

	#------------------------------------------------------------------------------
	# This method compiles the subroutines
	def compileSubroutine(self):
		self.of.write((self.space*self.spaceCount)+self.xml['subroutineDecb']+'\n')
		self.spaceCount += 1

		while self.token.hasMoreTokens:
			tokentype = self.token.tokenType()
			if self.keyword in tokentype:
				tempkey = self.token.keyWord()
				if self.key_method in tempkey or self.key_function in tempkey or self.key_constructor in tempkey:
					self.of.write((self.space*self.spaceCount)+self.xml['keywordb']+tempkey.lower()+self.xml['keyworde']+'\n')

				elif self.key_int in tempkey or self.key_char in tempkey or self.key_boolean in tempkey or self.key_void in tempkey:
					self.of.write((self.space*self.spaceCount)+self.xml['keywordb']+tempkey.lower()+self.xml['keyworde']+'\n')

				elif self.key_var in tempkey:
					self.compileVarDec()

				else:
					break

			elif self.sym in tokentype:
				tempsym = self.token.symbol()
				if '(' in tempsym:
					self.of.write((self.space*self.spaceCount)+self.xml['symbolb']+tempsym+self.xml['symbole']+'\n')
					self.token.advance()
					self.compileParameterList()
					self.of.write((self.space*self.spaceCount)+self.xml['subroutineBodyb']+'\n')
					self.of.write((self.space*self.spaceCount)+self.xml['symbolb']+self.token.symbol()+self.xml['symbole']+'\n')
				else:
					self.of.write((self.space*self.spaceCount)+self.xml['symbolb']+tempsym+self.xml['symbole']+'\n')

			elif self.ident in tokentype:
				self.of.write((self.space*self.spaceCount)+self.xml['identifierb']+self.token.identifier()+self.xml['identifiere']+'\n')

			self.token.advance()

		self.compileStatements()

		self.of.write((self.space*self.spaceCount)+self.xml['subroutineBodye']+'\n')

		self.spaceCount -= 1
		self.of.write((self.space*self.spaceCount)+self.xml['subroutineDece']+'\n')

	#------------------------------------------------------------------------------
	# This method compiles the parameter list
	def compileParameterList(self):
		self.of.write((self.space*self.spaceCount)+self.xml['parameterListb']+'\n')
		self.spaceCount += 1

		while self.token.hasMoreTokens():
			tokentype = self.token.tokenType()

			if self.keyword in tokentype:
				tempkey = self.token.keyWord()
				self.of.write((self.space*self.spaceCount)+self.xml['keywordb']+tempkey.lower()+self.xml['keyworde']+'\n')

			elif self.ident in tokentype:
				tempident = self.token.identifier()
				self.of.write((self.space*self.spaceCount)+self.xml['identifierb']+tempident+self.xml['identifiere']+'\n')

			elif self.sym in tokentype:
				tempsym = self.token.symbol()
				if ')' in tempsym:
					break

				elif ',' in tempsym:
					self.of.write((self.space*self.spaceCount)+self.xml['symbolb']+tempsym+self.xml['symbole']+'\n')

				else:
					print(self.token.errorMsg())
					sys.exit(0)
			
			self.token.advance()

		self.spaceCount -= 1
		self.of.write((self.space*self.spaceCount)+self.xml['parameterListe']+'\n')
		self.of.write((self.space*self.spaceCount)+self.xml['symbolb']+tempsym+self.xml['symbole']+'\n')
		self.token.advance()
		self.token.advance()

	#------------------------------------------------------------------------------
	# This method compiles the var decliration
	def compileVarDec(self):
		self.of.write((self.space*self.spaceCount)+self.xml['varDecb']+'\n')
		self.spaceCount += 1

		has_var_dec = False

		while self.token.hasMoreTokens():
			tokentype = self.token.tokenType()

			if self.keyword in tokentype:
				tempkey = self.token.keyWord()
				if self.key_var in tempkey:
					self.of.write((self.space*self.spaceCount)+self.xml['keywordb']+tempkey.lower()+self.xml['keyworde']+'\n')

				elif self.key_int in tempkey or self.key_char in tempkey or self.key_boolean in tempkey:
					self.of.write((self.space*self.spaceCount)+self.xml['keywordb']+tempkey.lower()+self.xml['keyworde']+'\n')

				else:
					break

			elif self.ident in tokentype:
				tempident = self.token.identifier()
				self.of.write((self.space*self.spaceCount)+self.xml['identifierb']+tempident+self.xml['identifiere']+'\n')

			elif self.sym in tokentype:
				tempsym = self.token.symbol()
				if ',' in tempsym:
					self.of.write((self.space*self.spaceCount)+self.xml['symbolb']+tempsym+self.xml['symbole']+'\n')
				elif ';' in tempsym:
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
				if self.key_let in tempkey:
					self.compileLet()

				elif self.key_if in tempkey:
					self.compileIf()
					continue

				elif self.key_while in tempkey:
					self.compileWhile()

				elif self.key_do in tempkey:
					self.compileDo()

				elif self.key_return in tempkey:
					self.compileReturn()

				else:
					print(self.token.errorMsg())
					sys.exit(0)
			elif self.sym in tokentype:
				tempsym = self.token.symbol()
				if '}' in tempsym:
					break
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
		subCallb = True

		while self.token.hasMoreTokens():
			tokentype = self.token.tokenType()
			if self.keyword in tokentype:
				tempkey = self.token.keyWord()
				if self.key_do in tempkey:
					self.of.write((self.space*self.spaceCount)+self.xml['keywordb']+tempkey.lower()+self.xml['keyworde']+'\n')
				else:
					print(self.token.errorMsg())
					sys.exit(0)

			elif self.ident in tokentype:
				self.compileExpression(True)
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
				else:
					print(self.token.errorMsg())
					sys.exit(0)

			elif self.ident in tokentype:
				tempident = self.token.identifier()
				self.of.write((self.space*self.spaceCount)+self.xml['identifierb']+tempident+self.xml['identifiere']+'\n')

			elif self.sym in tokentype:
				tempsym = self.token.symbol()
				if '[' in tempsym:
					self.of.write((self.space*self.spaceCount)+self.xml['symbolb']+tempsym+self.xml['symbole']+'\n')
					self.token.advance()
					self.compileExpression(False)
					self.of.write((self.space*self.spaceCount)+self.xml['symbolb']+self.token.symbol()+self.xml['symbole']+'\n')
					self.token.advance()
					continue

				elif '=' in tempsym:
					self.of.write((self.space*self.spaceCount)+self.xml['symbolb']+tempsym+self.xml['symbole']+'\n')
					self.token.advance()
					self.compileExpression(False)
					tempsym = self.token.symbol()
				
				if ';' in self.token.symbol():
					self.of.write((self.space*self.spaceCount)+self.xml['symbolb']+tempsym+self.xml['symbole']+'\n')
					break
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
				else:
					print(self.token.errorMsg())
					sys.exit(0)

			elif self.sym in tokentype:
				tempsym = self.token.symbol()
				if '(' in tempsym:
					self.of.write((self.space*self.spaceCount)+self.xml['symbolb']+tempsym+self.xml['symbole']+'\n')
					self.token.advance()
					self.compileExpression(False)
					self.of.write((self.space*self.spaceCount)+self.xml['symbolb']+self.token.symbol()+self.xml['symbole']+'\n')
				elif '{' in tempsym:
					self.of.write((self.space*self.spaceCount)+self.xml['symbolb']+tempsym+self.xml['symbole']+'\n')
					self.token.advance()
					self.compileStatements()
					break
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

				else:
					self.compileExpression(False)
					self.of.write((self.space*self.spaceCount)+self.xml['symbolb']+self.token.symbol()+self.xml['symbole']+'\n')
					self.token.advance()
					break

			elif self.ident in tokentype or self.string_c in tokentype or self.intc in tokentype:
				self.compileExpression(False)
				self.of.write((self.space*self.spaceCount)+self.xml['symbolb']+self.token.symbol()+self.xml['symbole']+'\n')
				self.token.advance()
				break

			elif self.sym in tokentype:
				tempsym = self.token.symbol()
				if ';' in tempsym:
					self.of.write((self.space*self.spaceCount)+self.xml['symbolb']+tempsym+self.xml['symbole']+'\n')
					break
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

		seen_once = True

		while self.token.hasMoreTokens():
			tokentype = self.token.tokenType()
			if self.keyword in tokentype:
				tempkey = self.token.keyWord()
				if self.key_if in tempkey and seen_once:
					self.of.write((self.space*self.spaceCount)+self.xml['keywordb']+tempkey.lower()+self.xml['keyworde']+'\n')
					seen_once = False

				elif self.key_else in tempkey:
					self.of.write((self.space*self.spaceCount)+self.xml['keywordb']+tempkey.lower()+self.xml['keyworde']+'\n')

				else:
					break

			elif self.sym in tokentype:
				tempsym = self.token.symbol()
				if '(' in tempsym:
					self.of.write((self.space*self.spaceCount)+self.xml['symbolb']+tempsym+self.xml['symbole']+'\n')
					self.token.advance()
					self.compileExpression(False)
					self.of.write((self.space*self.spaceCount)+self.xml['symbolb']+self.token.symbol()+self.xml['symbole']+'\n')

				elif '{' in tempsym:
					self.of.write((self.space*self.spaceCount)+self.xml['symbolb']+tempsym+self.xml['symbole']+'\n')
					self.token.advance()
					self.compileStatements()

			self.token.advance()

		self.spaceCount -= 1
		self.of.write((self.space*self.spaceCount)+self.xml['ifStatemente']+'\n')

	#------------------------------------------------------------------------------
	# This method compiles the expression
	def compileExpression(self,subCall):
		if not subCall:
			self.of.write((self.space*self.spaceCount)+self.xml['expressionb']+'\n')
		self.spaceCount += 1

		while self.token.hasMoreTokens():
			tokentype = self.token.tokenType()
			if self.sym in tokentype:
				tempsym = self.token.symbol()
				if tempsym in '+-*/&|<>=':
					if '<' in tempsym:
						self.of.write((self.space*self.spaceCount)+self.xml['symbolb']+"&lt;"+self.xml['symbole']+'\n')
					elif '>' in tempsym:
						self.of.write((self.space*self.spaceCount)+self.xml['symbolb']+"&gt;"+self.xml['symbole']+'\n')
					elif '&' in tempsym:
						self.of.write((self.space*self.spaceCount)+self.xml['symbolb']+"&amp;"+self.xml['symbole']+'\n')
					else:
						self.of.write((self.space*self.spaceCount)+self.xml['symbolb']+tempsym+self.xml['symbole']+'\n')

				elif tempsym in '(~':
					self.compileTerm(subCall)

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
				
				else:
					print(self.token.errorMsg())
					sys.exit(0)

			elif self.ident in tokentype:
				tempident = self.token.identifier()
				peaks = self.token.peak()
				if '.' in peaks:
					#replace this with code to do a look up
					self.of.write((self.space*self.spaceCount)+self.xml['identifierb']+tempident+self.xml['identifiere']+'\n')
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

					self.compileExpressionList()

				elif '(' in peaks:

					self.of.write((self.space*self.spaceCount)+self.xml['identifierb']+tempident+self.xml['identifiere']+'\n')
					self.token.advance()
					
					tempsym = self.token.symbol()
					self.of.write((self.space*self.spaceCount)+self.xml['symbolb']+tempsym+self.xml['symbole']+'\n')
					self.token.advance()

					self.compileExpressionList()

				elif '[' in peaks:
					self.of.write((self.space*self.spaceCount)+self.xml['identifierb']+tempident+self.xml['identifiere']+'\n')
					self.token.advance()
					
					tempsym = self.token.symbol()
					self.of.write((self.space*self.spaceCount)+self.xml['symbolb']+tempsym+self.xml['symbole']+'\n')
					self.token.advance()

					self.compileExpression(subCall)

					tempsym = self.token.symbol()
					self.of.write((self.space*self.spaceCount)+self.xml['symbolb']+tempsym+self.xml['symbole']+'\n')
				else:
					self.of.write((self.space*self.spaceCount)+self.xml['identifierb']+tempident+self.xml['identifiere']+'\n')

			elif self.intc in tokentype:
				self.of.write((self.space*self.spaceCount)+self.xml['integerConstantb']+self.token.intVal()+self.xml['integerConstante']+'\n')

			elif self.string_c in tokentype:
				self.of.write((self.space*self.spaceCount)+self.xml['StringConstantb']+self.token.stringVal()+self.xml['StringConstante']+'\n')

			elif self.sym in tokentype:
				tempsym = self.token.symbol()
				if '(' in tempsym:
					self.of.write((self.space*self.spaceCount)+self.xml['symbolb']+tempsym+self.xml['symbole']+'\n')
					self.token.advance()
					self.compileExpression(subCall)

					tempsym = self.token.symbol()
					self.of.write((self.space*self.spaceCount)+self.xml['symbolb']+tempsym+self.xml['symbole']+'\n')

				elif '~' in tempsym:
					self.of.write((self.space*self.spaceCount)+self.xml['symbolb']+tempsym+self.xml['symbole']+'\n')
					self.token.advance()
					self.compileTerm(subCall)

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
				if ',' in tempsym:
					self.of.write((self.space*self.spaceCount)+self.xml['symbolb']+tempsym+self.xml['symbole']+'\n')
					self.token.advance()
					self.compileExpression(False)
				elif ')' in tempsym:
					break
				else:
					self.compileExpression(False)
			else:
				self.compileExpression(False)

		self.spaceCount -= 1
		self.of.write((self.space*self.spaceCount)+self.xml['expressionListe']+'\n')
		self.of.write((self.space*self.spaceCount)+self.xml['symbolb']+self.token.symbol()+self.xml['symbole']+'\n')
