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
	linNum=0

	blockcom=False

	neOf=True

	#--------------------------------------------------------------------------
	# Class declaration:
	#--------------------------------------------------------------------------
	
	#--------------------------------------------------------------------------
	# Contstructor
	def __init__(self,infile):
		self.file_in = infile
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
	def tokenType(self):
		return self.curToken

	#--------------------------------------------------------------------------
	# Returns the symbol as a char
	def symbol(self):
		return self.curSym

	#--------------------------------------------------------------------------
	# Returns the current identifier
	def identifier(self):
		return self.curIdent

	#--------------------------------------------------------------------------
	# Returns the current int val
	def intVal(self):
		return self.curInt

	#--------------------------------------------------------------------------
	# Returns the current string val
	def stringVal(self):
		return self.curString
		
	#--------------------------------------------------------------------------
	# Advance reading of file
	def advance(self):
		
		if len(self.line) == 0 or self.blockcom:
			self.curToken = "NILL"
			#checks for EOF
			temp = self.read.tell()
			self.line = self.read.readline()
			if temp == self.read.tell():
				self.read.close()
				self.neOf=False
				return
			self.linNum += 1
			self.line = self.line.strip()
			
			if len(self.line) == 0:
				self.curToken='NILL'

			if re.search('^\/\/',self.line) is not None:
				self.line = ''
				self.curToken='NILL'

			if re.search('\*\/',self.line) is not None and self.blockcom:
				self.blockcom = False
				tempd = re.search('(.*\*\/)(.*)',self.line)
				self.line = tempd.group(2)
				self.curToken='NILL'

			elif self.blockcom:
				self.line = ''
				self.curToken='NILL'

			if re.search('^\/\*\*.*\*\/',self.line) is not None:
				self.line = ''
				self.curToken = 'NILL'
			elif re.search('^\/\*\*',self.line) is not None:
				self.line = ''
				self.blockcom = True
				self.curToken='NILL'
		else:
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
	
			elif re.search('^\/\/',self.line) is not None:
				self.line = ''
				self.curToken='NILL'

			elif re.search('^\/\*\*',self.line) is not None:
				self.line = ''
				self.blockcom = True
				self.curToken='NILL'

			elif re.search('^[\(\)\{\}\[\]\.\,\;\+\-\*\/\&\<\>\=\~]{1}',self.line) is not None:
				temp = re.search('(^[\(\)\{\}\[\]\.\,\;\+\-\*\/\&\<\>\=\~]{1})',self.line)
				self.curToken = self.idents['sym']
				self.curSym = temp.group(1)
				self.line = re.sub('^[\(\)\{\}\[\]\.\,\;\+\-\*\/\&\<\>\=\~]{1}',' ',self.line)
	
			elif re.search('^[0-9]+',self.line) is not None:
				temp = re.search('(^[0-9]+)',self.line)
				self.curToken = self.idents['intc']
				self.curInt = temp.group(1)
				self.line = re.sub('^[0-9]+',' ',self.line)
	
			elif re.search('^\".*\"',self.line) is not None:
				temp = re.search('(^\")(.*)(\")',self.line)
				self.curToken = self.idents['string_c']
				self.curString = temp.group(2

					)
				self.line = re.sub('^\".*\"',' ',self.line)

			else:
				self.curToken = 'NILL'

	#--------------------------------------------------------------------------
	# peaks ahead to the next token
	def peak(self):
		if len(self.line) != 0:
			if re.search('^\.\(\[\]\)\;',self.line) is not None:
				temp = re.search('(^\.\(\[\]\)\;)(.*)',self.line)
				return temp.group(1)
			else:
				return 'NILL'
		else:
			return 'NILL'

	#--------------------------------------------------------------------------
	# This returns the error message
	def errorMsg(self):
		temp = "In file: "+self.file_in+'\n'
		temp += "On line "+repr(self.linNum)+'\n'
		temp += "Grammera violation before > '"+self.line+"'\n"
		return temp