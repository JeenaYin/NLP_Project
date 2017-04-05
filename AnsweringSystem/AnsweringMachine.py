#!/usr/bin/python

# Philip Dominici, Ryan Sickles

# April 2017
# Question answering program for 11441 semester project


import os, sys
import re
import string
import math
import numpy
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

	def __init__(self, question, document):
		# unpack question from txt file to string
		with open(question, 'r') as f:
			questionString = f.read()
			questionString = clean(questionString)
		self.question = questionString
		self.document = document
		self.wh = "who what when where"

	# remove punctuation
	def clean(self, s):
		cleanString = s.translate(None, string.punctuation)
		return(cleanString)

	def answerQuestion(self):
		# st = StanfordPOSTagger('english-bidirectional-distsim.tagger')
		# tags = st.tag('What is the airspeed of an unladen swallow ?'.split())
		#text = pos_tagger.tag(word_tokenize("What's the airspeed of an unladen swallow ?"))
		#print(text)

		# all the question tags we will consider
		searchObj = re.findall(r'did|was|is|who|what|where|when|how', self.question, re.I)
		qType = None
		if (len(searchObj) == 1):
			qType = searchObj[0]
		else:
			for (word in searchObj):
				if ((word in self.wh) and (qType == None)):
					qType = word
			if (qType == None): qType = searchObj[0]
		if (qType in self.wh):
			self.answerWh
		else: 
			self.answerBinary

	# consider binary (yes or no) questions
	def answerBinary(self):
		answer = False
		phraseOfInterest = ""
		# figure out the question-phrase we are interested in
		questionRelations = None
		if (len(questionRelations) > 1): # how to pick the relation of interest?
			pass
		# figure out the relations of the sentence
		sentenceRelations = None
		# check the relations of the sentence for the specific question phrase
		for (relation in relations):
			if (phraseOfInterest in relation): 
				answer = True
		return(answer)

	# consider wh- (subject specific) questions
	def answerWh(self, wh):
		return()

	def run(self):
		self.answerQuestion()

if __name__ == '__main__':
	AnsweringMachine(question=sys.argv[1], document=sys.argv[2]).run()