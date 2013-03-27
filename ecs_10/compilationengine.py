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
# Subroutines:
#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
# This method tokenizes the imput file
def tokenize(file):


#------------------------------------------------------------------------------
# Check user input:
#------------------------------------------------------------------------------



#------------------------------------------------------------------------------
# MAIN:
#------------------------------------------------------------------------------



#-----------------------End program--------------------------------------------