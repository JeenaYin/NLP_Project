import os 
import nltk
from nltk.parse import stanford
from nltk import word_tokenize, pos_tag
from nltk.tag.stanford import StanfordNERTagger
import re

directory = "/Users/charisseharuta/Documents/CMU/Spring2017/NLP/stanford-ner-2015-04-20"

class Sentences:
	def __init__(self, content):

		# raw = content.strip().decode("ascii", "ignore").encode("ascii")
		raw = content.strip()
		# raw2 = raw.decode('ascii', 'ignore')
		# raw = raw1.encode('ascii')
		self.pronoun = get_proN(raw)
		self.sentences = nltk.tokenize.sent_tokenize(content)
		self.size = len(self.sentences)
		tokenizedSentences = []
		for s in self.sentences:
			tokenizedSentences.append(word_tokenize(s))
		self.tokenSent = tokenizedSentences

		# self.ner_tags =
		# self.when_tags = 
		# self.pos_tags = 



def get_proN(raw):
	pNounCounts = dict()
	tokenized = word_tokenize(raw)
	os.environ['CLASSPATH'] = directory
	ner_tags = StanfordNERTagger(directory+"/classifiers/english.all.3class.distsim.crf.ser.gz").tag(tokenized)
	for (w, t) in ner_tags:
		print(w, t)
		# words are represented as (word, tag)
		if t == "PERSON":
			if(w not in pNounCounts):
				pNounCounts[w] = 1
			else:
				pNounCounts[w] +=1
	maxWord = "";
	maxCount = 0;
	for k in pNounCounts:
		if maxCount < pNounCounts[k]:
			maxCount = pNounCounts[k]
			maxWord = k
	print(maxWord)
	return maxWord



#testing
sentences = "Hello New York I like Sarah Newton Paris Paris"

testSent = Sentences(sentences)





