#!/usr/bin/python

# Philip Dominici, Ryan Sickles

# April 2017
# Question answering program for 11441 semester project
 

import os, sys
import string
import math
import numpy
from nltk.parse.stanford import StanfordParser
from nltk.parse.stanford import StanfordDependencyParser

class AnsweringMachine(object):

	def __init__(self, question, document):
		# unpack question from txt file to string
		with open(question, 'r') as f:
			questionString = f.read()
		self.question = questionString
		self.document = document

	def parse(self, sentence):
		parser = StanfordParser(model_path="edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz")
		# depParser = StanfordDependencyParser(model_path="edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz")
		parsedSentence = parser.raw_parse(sentence)
		return(parsedSentence)

	def answerQuestion(self):
		pass

	def run(self):
		self.answerQuestion()

if __name__ == '__main__':
    AnsweringMachine(question=sys.argv[1], document=sys.argv[2]).run()