#!/usr/bin/python

# Philip Dominici, Ryan Sickles

# April 2017
# Question answering program for 11441 semester project


import os, sys
import string
import math
import numpy
import nltk

class AnsweringMachine(object):

	def __init__(question, document):
		self.question = question
		self.document = document

	def assignTags(self, sentence):
		return(taggedSentence)

	def answerQuestion(self):
		pass

	def run(self):
		self.answerQuestion()

if __name__ == '__main__':
    AnsweringMachine(question=sys.argv[1], document=sys.argv[2]).run()