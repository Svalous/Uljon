import random

class Chain():
	def __init__(self, corpus, index):
		self.corpus = corpus
		self.index = index
	def next(self):
		current = self.index
		rand = random.randint(0, len(self.corpus[current])-1)
		self.index = (current[1], self.corpus[current][rand])
		return self.corpus[current][rand]
