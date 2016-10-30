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
			# TODO: Below should go to n - (avg time to .) or something more optimal
			# Perhaps look down the line one iteration to ensure that the sentence ends on time
			for x in range(0, n-1):
				self.sentence += gen.next() + ' '
			check = 0
			futile = False
			MAX_CHECK = 10
			while not futile:
				self.sentence += gen.end()
				# TODO: Figure out why I'm getting an exception right after this
				if self.sentence.find('.', beg=len(self.sentence)-2) > -1:
					check = MAX_CHECK
				else:
					self.sentence += ' '
				check += 1
				if check >= MAX_CHECK:
					futile = True
		except Exception:
			print('Oh no!')
			raise
		finally:
			f.close()
			return self.sentence
