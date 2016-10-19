import os
import re
import chain as mark

class Generator():
	def __init__(self, file):
		self.file = file 
		self.sentence = ''
	def makeSentence(self, n):
		try:
			f = open(self.file, 'r')
			lines = f.read()
			lines = re.sub(r'\n', r' ', lines)
			lineArr = lines.split(' ')
			lineArr = [x for x in lineArr if x != '']
			corpus = {}
			for x in range(0, len(lineArr) - 2):
				x0 = lineArr[x]
				x1 = lineArr[x+1]
				x2 = lineArr[x+2]
				try:
					corpus[(x0,x1)].append(x2)
				except KeyError:
					corpus[(x0,x1)] = [x2]
			gen = mark.Chain(corpus, list(corpus.keys())[0])
			for x in range(0, n):
				self.sentence += gen.next() + ' '
		except Exception:
			raise
		finally:
			f.close()
			return self.sentence
