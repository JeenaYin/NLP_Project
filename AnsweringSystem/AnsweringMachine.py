#!/usr/bin/python

# Philip Dominici, Ryan Sickles

# April 2017
# Question answering program for 11441 semester project


import os, sys
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
		self.question = questionString
		# answer is contained in sentence below
		self.document = document

	def parse(self, sentence):
		# parser = StanfordParser(model_path="edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz")
		# # depParser = StanfordDependencyParser(model_path="edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz")
		# parsedSentence = parser.raw_parse(sentence)
		return(parsedSentence)

	def answerQuestion(self):
		# st = StanfordPOSTagger('english-bidirectional-distsim.tagger')
		# tags = st.tag('What is the airspeed of an unladen swallow ?'.split())
		text = pos_tagger.tag(word_tokenize("What's the airspeed of an unladen swallow ?"))
		print(text)

	def run(self):
		self.answerQuestion()

if __name__ == '__main__':
	AnsweringMachine(question=sys.argv[1], document=sys.argv[2]).run()