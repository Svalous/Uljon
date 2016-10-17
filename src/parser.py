import os
import re
import chain as mark

fileName = input("Please enter the file in txt/ that you want to parse\t")
fullPath = os.path.dirname(os.path.abspath(__file__)) + "/txt/" + fileName
try:
	f = open(fullPath, 'r')
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
			print('reached')
		except KeyError:
			corpus[(x0,x1)] = [x2]
	print(corpus)
	gen = mark.Chain(corpus, list(corpus.keys())[0])
	for x in range(0, 30):
		print(gen.next(), end=' ')
	print()
except Exception:
	raise
finally:
	f.close()
