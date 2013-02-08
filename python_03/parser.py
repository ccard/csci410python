import sys, string, os, io
#Chris Card
#CS410
#Python02
#due:2/6/13
class Parser:
	#place in line
	lineplace = 0

	#state = 0 start of reading
	#state = 1 no comment starting character encountered
	#state = 2 / encountered
	#state = 3 / followed by / encountered
	#state = 4 / followed by * encountered
	#state = 5 * possibly indicating the end of comment
	#state = 6 * followed by / end of block comment
	#state = 7 eol comment state 3 ending with \n
	state = 0

	#line to print out
	lineout=''

	#line from file
	linein=''

	#is at end of file
	natend=True

	#the input file
	infile=''

	#counts for the old file summary
	charCount=0
	linCount=0
	block_count=0
	block_charCount=0
	eol_comments=0
	eol_charcount=0

	#counts for the summarry of the output file
	newCharCount=0
	newLinCount=0
	newBlock_count=0
	newBlock_charCount=0
	newEol_comments=0
	newEol_charcount=0

	def __init__(self,filein):
			self.filein = open(filein)
			infile = filein


	def isComment(self,curState, character):
		if character == '/':
			#This means that it has encountered / one before
			#this character
			if curState == 2:
				return 3
			#if it is still processing a comment
			elif curState == 3:
				return curState
			#means that it reached the end of a block comment
			elif curState == 5:
				return 6
			#it has just encountered a /
			else:
				return 2
		elif character == '*':
			#the start of a block comment
			if curState == 2:
				return 4
			#possibly is encountering the end of block comment
			elif curState == 4:
				return 5
			#in the middle of processing a block comment
			else:
				return curState
		elif character == '\n':
			#reached the end of EOL comment
			if curState == 3:
				return 7
			else:
				return curState
		else:
			#down grades the state if not end of block comment
			if curState == 5:
				return 4
			#down grades the state if not start of EOL comment
			elif curState == 2:
				return 1
			#start of processing the file
			elif curState == 0:
				return 1
			else:
				return curState

	def hasMoreCommands(self):
		return self.natend

	def advance(self):
		temp = self.filein.tell()
		self.linein = self.filein.readline()
		if temp == self.filein.tell():
			self.lineout=''
			self.filein.close()
			self.natend=False
			return

		self.linCount+=1
		self.lineout=''

		for c in  self.linein:
			self.charCount+=1
			self.state = self.isComment(self.state,c)
	
			if self.state == 2:
				self.lineout += c
	
			elif self.state == 3:
				self.lineout = ''
				self.eol_charcount+=1
	
			elif self.state == 7:
				self.state = 1
				self.eol_comments+=1
				self.lineout +='\n'
	
			elif self.state == 4 or self.state == 5:
				self.block_charCount+=1
				self.lineout=''
	
			elif self.state == 6:
				self.block_count+=1
				self.state = 1
				self.lineout+='\n'
	
			else:
				self.lineout+=c

		self.newCharCount+=len(self.lineout)
		self.newLinCount+=1

	def output(self):
		return self.lineout

	def stats(self):
		print('\t\tINPUT\t\tOUTPUT')
		print('Filename\t'+self.infile+'\t\t')
		print('Lines \t\t'+repr(self.linCount)+'\t\t'+repr(self.newLinCount))
		print('Characters\t'+repr(self.charCount)+'\t\t'+repr(self.newCharCount))
		print('Block comments\t'+repr(self.block_count)+'\t\t'+repr(self.newBlock_count))
		print('   characters\t'+repr(self.block_charCount)+'\t\t'+repr(self.newBlock_charCount))
		print('EOL comments\t'+repr(self.eol_comments)+'\t\t'+repr(self.newEol_comments))
		print('    characters\t'+repr(self.eol_charcount)+'\t\t'+repr(self.newEol_charcount))

