import random

class Chain():
	def __init__(self, corpus, index):
		self.corpus = corpus
		self.index = index
	def next(self):
		futile = False
		check = 0
		# Temporary structure for MVP...should end sentence if it reaches a KeyError
		while not futile:
			try:
				current = self.index
				rand = random.randint(0, len(self.corpus[current])-1)
				self.index = (current[1], self.corpus[current][rand])
				return self.corpus[current][rand]
			except KeyError:	
				pass
			finally:
				check += 1
				if check == 10:
					futile = True
					return ''
