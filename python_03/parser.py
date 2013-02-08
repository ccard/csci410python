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
	atend=False

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

	def __init__(self,filein,fileout):
			self.filein = open(filein)
			self.fileout = open(fileout,'w')


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
		return atend

	def advance(self):
		if len(linein) == lineplace:
			temp = self.filein.tell
			linein = self.filein.readline()
			if temp == self.filein.tell():
				return

