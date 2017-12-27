from markov_text3.db import Db
from markov_text3.gen import Generator
from markov_text3.parse import Parser
from markov_text3.sql import Sql
from markov_text3.rnd import Rnd
import sys
import sqlite3
import codecs

SENTENCE_SEPARATOR = '.'
WORD_SEPARATOR = ' '

def parse(name, depth, file_to_parse):
	
	db = Db(sqlite3.connect(name + '.db'), Sql())
	db.setup(depth)
		
	txt = codecs.open(file_to_parse, 'r', 'utf-8').read()
	Parser(name, db, SENTENCE_SEPARATOR, WORD_SEPARATOR).parse(txt)
	print('Database', name, 'created from', file_to_parse)

def generate(name, count):
	db = Db(sqlite3.connect(name + '.db'), Sql())
	generator = Generator(name, db, Rnd())
	markov_text = []
	for i in range(0, count):
		markov_text.append(generator.generate(WORD_SEPARATOR))

	return markov_text

def main():
	args = sys.argv
	usage = 'Usage: %s (parse <name> <depth> <path to txt file>|gen <name> <count>)' % (args[0], )

	if (len(args) < 3):
		raise ValueError(usage)

	mode  = args[1]
	name  = args[2]
	
	if mode == 'parse':
		if (len(args) != 5):
			raise ValueError(usage)
		
		depth = int(args[3])
		file_to_parse = args[4]
		parse(name, depth, file_to_parse)
				
	
	elif mode == 'gen':
		count = int(args[3])
		print(generate(name, count))
		
	
	else:
		raise ValueError(usage)

if __name__ == '__main__':
	main()