#!/usr/bin/python

# Philip Dominici, Ryan Sickles

# April 2017
# Question answering program for 11441 semester project


import os, sys
import re
import string
import math
import numpy
import nltk
from nltk.tag.stanford import StanfordPOSTagger
from nltk.parse.stanford import StanfordParser
from nltk.parse.stanford import StanfordDependencyParser
from nltk.tag import StanfordPOSTagger
from nltk import word_tokenize

# Add the jar and model via their path (instead of setting environment variables):
jar = '../stanford-postagger-2016-10-31/stanford-postagger.jar'
model = '../stanford-postagger-2016-10-31/models/english-left3words-distsim.tagger'
pos_tagger = StanfordPOSTagger(model, jar, encoding='utf8')


class AnsweringMachine(object):

	def __init__(self, questionDoc, sentenceDoc):
		# unpack question from txt file to string
		with open(questionDoc, 'r') as f:
			questionString = f.read()
			questionString = self.clean(questionString)
		self.question = questionString
		with open(sentenceDoc, 'r') as f:
			sentenceString = f.read()
			sentenceString = self.clean(sentenceString)
		self.sentence = sentenceString
		self.wh = "who what when where"

	# remove punctuation
	# input: STRING
	# output: STRING which is stripped
	def clean(self, s):
		translator = str.maketrans('', '', string.punctuation)
		cleanString = s.translate(translator)
		return(cleanString)

	# pass in a string to be tagged in NER
	# input: a STRING, the sentence to be evaluated
	# return: a LIST of TUPLES, each containing the word and its named entity
	def ner(self, sentence):
		#st = NERTagger('../stanford-ner/classifiers/all.3class.distsim.crf.ser.gz','../stanford-ner/stanford-ner.jar')
		rawEntities = nltk.ne_chunk(nltk.pos_tag(word_tokenize(sentence))).pos() # tree object
		entities = list()
		for ent in rawEntities:
			pureTuple = (ent[0][0], ent[1])
			entities.append(pureTuple)
		return(entities)

	def answerQuestion(self):
		# st = StanfordPOSTagger('english-bidirectional-distsim.tagger')
		# tags = st.tag('What is the airspeed of an unladen swallow ?'.split())
		#text = pos_tagger.tag(word_tokenize("What's the airspeed of an unladen swallow ?"))
		#print(text)

		# all the question tags we will cownsider
		searchObj = re.findall(r'did|was|is|who|what|where|when|how', self.question, re.I)
		qType = None
		if (len(searchObj) == 1):
			qType = searchObj[0]
		else:
			for word in searchObj:
				if ((word in self.wh) and (qType == None)):
					qType = word
			if (qType == None): qType = searchObj[0]
		# note that we are working in lower case to identify question types
		if (qType.lower() in self.wh):
			self.answerWh(qType.lower())
		else: 
			self.answerBinary()

	# consider binary (yes or no) questions
	def answerBinary(self):
		answer = False
		phraseOfInterest = ""
		# figure out the question-phrase we are interested in
		questionRelations = []
		if (len(questionRelations) > 1): # how to pick the relation of interest?
			pass
		# figure out the relations of the sentence
		sentenceRelations = []
		# check the relations of the sentence for the specific question phrase
		for relation in sentenceRelations:
			if (phraseOfInterest in relation): 
				answer = True
		return(answer)

	# consider wh- (subject specific) questions
	def answerWh(self, wh):
		print(wh)
		if (wh == "who"):
			questionEntities = self.ner(self.question)
			sentenceEntities = self.ner(self.sentence)
		if (wh == "where"):
			questionEntities = self.ner(self.question)
			sentenceEntities = self.ner(self.sentence)
		if (wh == "when"):
			questionEntities = self.ner(self.question)
			sentenceEntities = self.ner(self.sentence)
		print(questionEntities)

	def run(self):
		self.answerQuestion()

if __name__ == '__main__':
	AnsweringMachine(questionDoc=sys.argv[1], sentenceDoc=sys.argv[2]).run()