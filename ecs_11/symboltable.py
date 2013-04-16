import sys, string, os, io,re
#------------------------------------------------------------------------------
#Chris Card
#CS410
#ECS project 10
#python 3.3
#Due:3/25/13
#This is stores the symbol table for each class
#------------------------------------------------------------------------------

class SymbolTable:

	#--------------------------------------------------------------------------
	# Var Dec:
	#--------------------------------------------------------------------------

	#------Class scope tables--------------------------------------------------
	kindClass = {'':''}
	typeClass = {'':''}
	indexClass = {'':''}

	classStatic = 0
	classHeap = 0

	#----------Subroutine scope------------------------------------------------
	kindSub = {'':''}
	typeSub = {'':''}
	indexSub = {'':''}

	subArg = 0
	subVar = 0



	#--------------------------------------------------------------------------
	# Class Dec:
	#--------------------------------------------------------------------------

	def __init__(self):
		self.ji=""

	#--------------------------------------------------------------------------
	# This clears all subrouting tables (chaging the scope)
	def startSubroutine(self):
		self.kindSub.clear()
		self.typeSub.clear()
		self.indexSub.clear()
		self.subArg = 0
		self.subVar = 0

	#--------------------------------------------------------------------------
	# This defines a new identifier
	def Define(self,name,typeof,kind):
		if 'STATIC' in kind or 'FIELD' in kind:
			self.typeClass[name] = typeof
			self.kindClass[name] = kind

			if 'STATIC' in kind:
				self.indexClass[name] = self.classStatic
				self.classStatic += 1

			else:
				self.indexClass[name] = self.classHeap
				self.classHeap += 1

		else:
			self.typeSub[name] = typeof
			self.kindSub[name] = kind

			if 'ARG' in kind:
				self.indexSub[name] = self.subArg
				self.subArg += 1

			else:
				self.indexClass[name] = self.subVar
				self.subVar += 1

	#--------------------------------------------------------------------------
	# This returns the number of variables with a given kind
	def varCount(self,kind):
		if 'STATIC' in kind or 'FIELD' in kind:
			#count of the class heap because static is never need to be counted
			count = self.classHeap

			return count

		else:
			count = 0
			for k in self.kindSub.values():
				if k in kind:
					count += 1

			return count

	#--------------------------------------------------------------------------
	# This Method returns the kind of a identifier
	def kindOf(self,name):
		#check subroutine scope first then class scope
		if name in self.kindSub:
			return self.kindSub[name]

		elif name in self.kindClass:
			return self.kindClass[name]

		else:
			return "NONE"

	#--------------------------------------------------------------------------
	# This returns the type of an identifier
	def typeOf(self,name):
		#check subroutine scope first then class scope
		if name in self.typeSub:
			return self.typeSub[name]

		elif name in self.typeClass:
			return self.typeClass[name]

		else:
			return "NONE"

	#--------------------------------------------------------------------------
	# This returns the index of an identifier
	def indexOf(self,name):
		#check subroutine scope first then class scope
		if name in self.indexSub:
			return self.indexSub[name]

		elif name in self.indexClass:
			return self.indexClass[name]

		else:
			return "NONE"