import sys, string, os, io,re
#------------------------------------------------------------------------------
#Chris Card
#CS410
#ECS project 06
#Due:2/25/13
#------------------------------------------------------------------------------

class SymbolTable:

	#constants
	symbol_table={'SP':'0000000000000000','LCL':'0000000000000001','ARG':'0000000000000010',
			'THIS':'0000000000000011','THAT':'0000000000000100','R0':'0000000000000000',
			'R1':'0000000000000001','R2':'0000000000000010','R3':'0000000000000011',
			'R4':'0000000000000100','R5':'0000000000000101','R6':'0000000000000110',
			'R7':'0000000000000111','R8':'0000000000001000','R9':'0000000000001001',
			'R10':'0000000000001010','R11':'0000000000001011','R12':'0000000000001100',
			'R13':'0000000000001101','R14':'0000000000001110','R15':'0000000000001111',
			'SCREEN':'0100000000000000','KBD':'0110000000000000'}

	def __init__(self):
		pass

	#--------------------------------------------------------------------------
	# Looks up symbol if it isn't there adds it
	def addEntry(self,sym,address,is_user):
		sym=sym.strip('()')
		bi = bin(address) #Converts to binary
		bi = bi.lstrip('-0b') #Strips -0b of the front
		dif = 16 - len(bi) #Calcs number of high order 0's need to make 16bit
		bi = '0'*dif+bi #Pads with high order 0's
		if is_user:
			self.symbol_table[sym]='('+sym+')'+bi
		else:
			self.symbol_table[sym]=bi

	#--------------------------------------------------------------------------
	# checks to see symbol table contains the entry
	def contains(self,sym):
		if sym in self.symbol_table:
			return True
		return False

	#--------------------------------------------------------------------------
	# gets the address
	def getAddress(self,sym):
		sym =sym.strip('()')
		return self.symbol_table[sym]
