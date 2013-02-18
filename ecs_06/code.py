import sys, string, os, io,re
#------------------------------------------------------------------------------
#Chris Card
#CS410
#ECS project 06
#Due:2/25/13
#------------------------------------------------------------------------------

class Code:

	#Constance
	comp_table={'0':'101010','1':'111111','-1':'111010','D':'001100',
			'A':'110000', 'M':'110000', '!D':'001101','!A':'110001',
			'!M':'110001','-D':'001111','-A':'110011', '-M':'110011',
			'D+1':'011111','A+1':'110111', 'M+1':'110111', 'D-1':'001110',
			'A-1':'110010','M-1':'110010','D+A':'000010','D+M':'000010',
			'D-A':'010011', 'D-M':'010011','A-D':'000111', 'M-D':'000111',
			'D&A':'000000','D&M':'000000','D|A':'010101','D|M':'010101'}

	dest_table={'null':'000','M':'001','D':'010','MD':'011','A':'100','AM':'101',
				'AD':'110','AMD':'111'}
	
	extended_dest_table={'DM':'011','MA':'101','DA':'110','MDA':'111','DAM':'111',
						'MAD':'111','DMA':'111','ADM':'111'}
	
	jump_table={'null':'000','JGT':'001','JEQ':'010','JGE':'011','JLT':'100',
				'JNE':'101','JLE':'110','JMP':'111'}



	def __init__(self):
		pass

	#------------------------------------------------------------------------------
	# Looks up comp in comp_table if it isn't there reports error and exits
	def comp(self,comp,line):
		if comp in self.comp_table:
			return self.comp_table[comp]
		else:
			print('Unrecognized command '+comp+' on line: '+repr(line)+' !')
			sys.exit(0)
	
	#------------------------------------------------------------------------------
	# Looks up dest in dest_table(or extended_dest_table) if it isn't there reports
	# error and exits
	def dest(self,dest,line,extend_dest):
		if dest in self.dest_table:
			return self.dest_table[dest]
		else:
			#If we are to look in the extended_dest_table
			if extend_dest:
				if dest in self.extended_dest_table:
					return self.extended_dest_table[dest]
	
			print('Unrecognized destination '+dest+' on line: '+repr(line)+' !')
			sys.exit(0)
	
	#------------------------------------------------------------------------------
	# This looks up jump commands and returns the appropriate bit sequence
	def jump(self,jump,line):
		if jump in self.jump_table:
			return self.jump_table[jump]
		else:
			print('Unrecognized jump'+jump+' on line: '+repr(line)+' !')
			sys.exit(0)