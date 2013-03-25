import sys, string, os, io,re
#------------------------------------------------------------------------------
#Chris Card
#CS410
#ECS project 10
#python 3.3
#Due:3/25/13
#This tokenizes the jack file
#------------------------------------------------------------------------------

class JackToken:

	#--------------------------------------------------------------------------
	# Var delcar:
	#--------------------------------------------------------------------------

	key_words= {'class':'CLASS','method':'METHOD','function':'FUNCTION',
				'constructor':'CONSTRUCTOR','int':'INT','boolean':'BOOLEAN',
				'char':'CHAR','void':'VOID','var':'VAR','static':'STATIC','field':'FIELD',
				'let':'LET','do':'DO','if':'IF','else':'ELSE','while':'WHILE',
				'return':'RETURN','true':'TRUE','false':'FALSE','null':'NULL','this':'THIS'}
	idents = {'key':'KEYWORD','sym':'SYMBOL','ident':'IDENTIFIER','intc':'INT_CONST',
				'string_c':'STRING_CONST'}

	line=''
	curToken=''
	curKey = ''
	curSym=''
	curIdent=''
	curInt=''
	curString=''

	blockcom=False

	neOf=True

	#--------------------------------------------------------------------------
	# Class declaration:
	#--------------------------------------------------------------------------
	
	#--------------------------------------------------------------------------
	# Contstructor
	def __init__(self,infile):
		self.read = open(infile)

	#--------------------------------------------------------------------------
	# Returns true if it has more to read
	def hasMoreTokens(self):
		return self.neOf

	#--------------------------------------------------------------------------
	# Returns returns the keyword
	def keyWord(self):
		return self.curKey

	#--------------------------------------------------------------------------
	# Returns the current token type
	def tokeType(self):
		return self.curToken

	#--------------------------------------------------------------------------
	# Returns the symbol as a char
	def symbol(self):
		return self.curSym

	#--------------------------------------------------------------------------
	# returns the current identifier
	#--------------------------------------------------------------------------
	# Advance reading of file
	def advance(self):
		
		if len(self.line) == 0 or blockcom:
			#checks for EOF
			temp = self.read.tell()
			self.line = self.read.readline()
			if temp == self.read.tell():
				self.read.close()
				self.neOf=False
				return
			self.line = self.line.strip()
			if re.search('^\/\/',self.line) is not None:
				self.line = ''
				self.advance()

			if re.search('\*\/',self.line) is not None and blockcom:
				blockcom = False
				tempd = re.search('(.+\*\/)(.*)',self.line)
				self.line = tempd.group(2)
				self.advance()
			elif blockcom:
				self.line = ''
				self.advance()

			if re.search('^\/\*\*',self.line) is not None:
				self.line = ''
				blockcom = True
				self.advance()
				
		self.line = self.line.strip()

		if re.search('^[A-Za-z\_]+[A-Za-z\_0-9]*',self.line) is not None:
			temp = re.search('(^[A-Za-z\_]+[A-Za-z\_0-9]*)',self.line)
			if temp.group(1) in self.key_words:
				self.curToken = self.idents['key']
				self.curKey = self.key_words[temp.group(1)]
			else:
				self.curToken = self.idents['ident']
				self.curIdent = temp.group(1)
			self.line = re.sub('^[A-Za-z\_]+[A-Za-z\_0-9]*',' ',self.line)

		elif re.search('^\(\)\{\}\[\]\.\,\;\+\-\*\/\&\<\>\=\~')