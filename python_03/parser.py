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
		return natend

	def advance(self):
		if len(linein) == lineplace:
			temp = self.filein.tell
			linein = self.filein.readline()
			if temp == self.filein.tell():
				self.filein.close()
				natend=False
				return

			else:
				linCount+=1
				newEol_charcount+=len(lineout)
				newLinCount+=1
				lineout=''

		for c in  linein:
			charCount+=1
			state = isComment(state,c)
	
			if state == 2:
				lineout += c
	
			elif state == 3:
				lineout = ''
				eol_charcount+=1
	
			elif state == 7:
				state = 1
				eol_comments+=1
				lineout +='\n'
	
			elif state == 4 or state == 5:
				block_charCount+=1
				lineout=''
	
			elif state == 6:
				block_count+=1
				state = 1
				lineout+='\n'
	
			else:
				lineout+=c

	def output(self):
		return lineout

	def stats(self):
		print('\t\tINPUT\t\tOUTPUT')
		print('Filename\t'+infile+'\t\t')
		print('Lines \t\t'+repr(linCount)+'\t\t'+repr(newLinCount))
		print('Characters\t'+repr(charCount)+'\t\t'+repr(newCharCount))
		print('Block comments\t'+repr(block_count)+'\t\t'+repr(newBlock_count))
		print('   characters\t'+repr(block_charCount)+'\t\t'+repr(newBlock_charCount))
		print('EOL comments\t'+repr(eol_comments)+'\t\t'+repr(newEol_comments))
		print('    characters\t'+repr(eol_charcount)+'\t\t'+repr(newEol_charcount))

