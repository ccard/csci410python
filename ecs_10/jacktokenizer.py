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

	#map for all the key words
	key_words= {'class':'CLASS','method':'METHOD','function':'FUNCTION',
				'constructor':'CONSTRUCTOR','int':'INT','boolean':'BOOLEAN',
				'char':'CHAR','void':'VOID','var':'VAR','static':'STATIC','field':'FIELD',
				'let':'LET','do':'DO','if':'IF','else':'ELSE','while':'WHILE',
				'return':'RETURN','true':'TRUE','false':'FALSE','null':'NULL','this':'THIS'}
	
	#map for all the token types
	idents = {'key':'KEYWORD','sym':'SYMBOL','ident':'IDENTIFIER','intc':'INT_CONST',
				'string_c':'STRING_CONST'}

	#stores the current line being readin
	line=''

	#current tokens keys, symbols, identifiers, ints, strings
	curToken=''
	curKey = ''
	curSym=''
	curIdent=''
	curInt=''
	curString=''

	#linnum to keep track of where in the file being read we are at
	#used for robust error detection
	linNum=0

	#if we are currently in the middle of reading a block comment
	blockcom=False

	#if we are not at EOF
	neOf=True

	#--------------------------------------------------------------------------
	# Class declaration:
	#--------------------------------------------------------------------------
	
	#--------------------------------------------------------------------------
	# Contstructor
	def __init__(self,infile):
		#stores the file being read in for robust error reporting
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
		#If we are done reading the line or in the middle of a block comment
		#read in a new line
		if len(self.line) == 0 or self.blockcom:
			#sets to NILL so that nothing is accidently written to the output
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
			
			#if an empty line was read in
			if len(self.line) == 0:
				self.curToken='NILL'
			#if line comment was read in
			if re.search('^\/\/',self.line) is not None:
				self.line = ''
				self.curToken='NILL'

			#if end of of block comment was read in
			if re.search('\*\/',self.line) is not None and self.blockcom:
				self.blockcom = False
				tempd = re.search('(.*\*\/)(.*)',self.line)
				self.line = tempd.group(2)
				self.curToken='NILL'

			#if we are still in the middle of a block comment
			elif self.blockcom:
				self.line = ''
				self.curToken='NILL'

			#if we run into a one line block comment
			if re.search('^\/\*\*.*\*\/',self.line) is not None:
				self.line = ''
				self.curToken = 'NILL'

			#if we run into start of a multi line block comment
			elif re.search('^\/\*\*',self.line) is not None:
				self.line = ''
				self.blockcom = True
				self.curToken='NILL'

		else:
			self.line = self.line.strip()

			#if an identifier is found
			if re.search('^[A-Za-z\_]+[A-Za-z\_0-9]*',self.line) is not None:
				temp = re.search('(^[A-Za-z\_]+[A-Za-z\_0-9]*)',self.line)

				#if the identifier happens to be a key word
				if temp.group(1) in self.key_words:
					self.curToken = self.idents['key']
					self.curKey = self.key_words[temp.group(1)]

				#other wise just an identifier
				else:
					self.curToken = self.idents['ident']
					self.curIdent = temp.group(1)

				#removes the current token form the line
				self.line = re.sub('^[A-Za-z\_]+[A-Za-z\_0-9]*','',self.line)
			
			#if the start of a line comment is found
			elif re.search('^\/\/',self.line) is not None:
				self.line = ''
				self.curToken='NILL'

			#if the start of a block comment is found
			elif re.search('^\/\*\*',self.line) is not None:
				self.line = ''
				self.blockcom = True
				self.curToken='NILL'

			#if a symbol is found
			elif re.search('^[\(\)\{\}\[\]\.\,\;\+\-\*\/\&\<\>\=\~]{1}',self.line) is not None:
				temp = re.search('(^[\(\)\{\}\[\]\.\,\;\+\-\*\/\&\<\>\=\~]{1})',self.line)
				self.curToken = self.idents['sym']
				self.curSym = temp.group(1)
				self.line = re.sub('^[\(\)\{\}\[\]\.\,\;\+\-\*\/\&\<\>\=\~]{1}','',self.line)
			
			#if a number is found
			elif re.search('^[0-9]+',self.line) is not None:
				temp = re.search('(^[0-9]+)',self.line)
				self.curToken = self.idents['intc']
				self.curInt = temp.group(1)
				self.line = re.sub('^[0-9]+','',self.line)
			
			#if a string constant is found
			elif re.search('^\".*\"',self.line) is not None:
				temp = re.search('(^\")(.*)(\")',self.line)
				self.curToken = self.idents['string_c']
				self.curString = temp.group(2)
				self.line = re.sub('^\".*\"','',self.line)

			#other wise nothing found
			else:
				self.curToken = 'NILL'

	#--------------------------------------------------------------------------
	# Peaks ahead to the next token, only returns symbols or nill
	def peak(self):
		self.line.strip()

		#if the current line is empty
		if len(self.line) != 0:
			#tries to find a symbol if it does it returns it
			if re.search('^[\.\(\[\]\)\;\+\-\*\/\&\|\<\>\=\,\~]{1}',self.line) is not None:
				temp = re.search('(\s*)(^[\.\(\[\]\)\;\+\-\*\/\&\|\<\>\=\,\~]{1})(.*)',self.line)
				return temp.group(2)
			else:
				return 'NILL'
		else:
			return 'NILL'

	#--------------------------------------------------------------------------
	# This returns the error message
	def errorMsg(self):
		temp = "In file: "+self.file_in+'\n'
		temp += "On line "+repr(self.linNum)+'\n'
		temp += "Grammar violation before > '"+self.line+"'\n"
		return temp