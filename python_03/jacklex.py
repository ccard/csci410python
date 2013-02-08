import sys, string, os, io
from parser import Parser

#checks the number of arguments passed in command line
if len(sys.argv) < 2:
	print("Incorrect number of arguments")
	print("JackLex.py <input file> <output file>")
	sys.exit(0);

inFile = sys.argv[1]
outFile = sys.argv[2]

Out = open(outFile,'w')

par = Parser(inFile)

while par.hasMoreCommands:
	par.advance()
	Out.write(par.output)

par.stats
Out.close()