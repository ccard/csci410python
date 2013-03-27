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
		,'identifierb':'<identifier>','identifiere':'</identifier>'}
	
	
	#------------------------------------------------------------------------------
	# This is the constructor
	def __init__(self,infile,outfile):
		self.of = open(outfile,'w')
		self.token = JackToken(infile)
	
	#------------------------------------------------------------------------------
	# This method compiles the class
	def compileClass(self):
		
	#------------------------------------------------------------------------------
	# This method compiles class var dec
	def compileClassVarDec(self):

	#------------------------------------------------------------------------------
	# This method compiles the subroutines
	def compileSubroutine(self):

	#------------------------------------------------------------------------------
	# This method compiles the parameter list
	def compileParameterList(self):

	#------------------------------------------------------------------------------
	# This method compiles the var decliration
	def compileVarDec(self):

	#------------------------------------------------------------------------------
	# This method compiles the statements
	def compileStatements(self):

	#------------------------------------------------------------------------------
	# This method compiles the do 
	def compileDo(self):

	#------------------------------------------------------------------------------
	# This method compiles the letStatement
	def compileLet(self):

	#------------------------------------------------------------------------------
	# This method compiles the whileStatement
	def compileWhile(self):

	#------------------------------------------------------------------------------
	# This method compiles the ReturnStatement
	def compileReturn(self):

	#------------------------------------------------------------------------------
	# This method compiles the ifStatement
	def compileIf(self):

	#------------------------------------------------------------------------------
	# This method compiles the expression
	def compileExpression(self):

	#------------------------------------------------------------------------------
	# This method compiles the term
	def compileTerm(self):

	#------------------------------------------------------------------------------
	# This method compiles the expressionList
	def compileExpressionList(self):