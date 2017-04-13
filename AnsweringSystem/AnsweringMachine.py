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
sys.path.append(os.path.abspath("../Dependencies/"))
import timex

# Add the jar and model via their path (instead of setting environment variables):
jar = '../stanford-postagger-2016-10-31/stanford-postagger.jar'
model = '../stanford-postagger-2016-10-31/models/english-left3words-distsim.tagger'
pos_tagger = StanfordPOSTagger(model, jar, encoding='utf8')


class AnsweringMachine(object):

	def __init__(self, questionDoc, sentenceDoc):
		# unpack question(s) and sentence(s) from txt files to strings
		self.questionList = []
		with open(questionDoc, 'r') as f:
			content = f.read()
			f.close()
		for question in content.splitlines():
			self.questionList.append(question)
		self.sentenceList = []
		with open(sentenceDoc, 'r') as f:
			content = f.read()
			f.close()
		for question in content.splitlines():
			self.sentenceList.append(question)
		# etc.
		self.wh = "who what when where"

	# remove punctuation
	# input: STRING
	# output: STRING which is stripped
	def clean(self, s):
		#translator = str.maketrans('', '', string.punctuation)
		#preppedString = s.translate(translator)
		#preppedString = s.replace(".", " punc").replace(",", " punc").replace("!", " punc").replace("?", " punc")
		preppedString = s.replace(".", " .").replace(",", " ,").replace("!", " !").replace("?", " ?").replace(";", " ;")
		preppedString = timex.timexTag(preppedString)
		return(preppedString)

	# pass in a string to be tagged in NER
	# input: a STRING, the sentence to be evaluated
	# return: a LIST of TUPLES, each containing the word and its named entity
	def ner(self, sentence):
		rawEntities = nltk.ne_chunk(nltk.pos_tag(word_tokenize(sentence))).pos() # tree object
		entities = list()
		for ent in rawEntities:
			pureTuple = (ent[0][0], ent[1])
			entities.append(pureTuple)
		return(entities)

	def answerQuestion(self, question, sentence):
		# all the question tags we will cownsider
		searchObj = re.findall(r'did|was|is|who|what|where|when|how', question, re.I)
		qType = None
		# if only one question-word, take that
		if (len(searchObj) == 1):
			qType = searchObj[0]
		# if >1 question-word, take first wh-words if exists, otherwise just take the first word
		else:
			for word in searchObj:
				if ((word in self.wh) and (qType == None)):
					qType = word
			if (qType == None): qType = searchObj[0]
		# note that we are working in lower case to identify question types
		if (qType.lower() in self.wh):
			answer = self.answerWh(qType.lower(), question, sentence)
		else: 
			answer = self.answerBinary()
		print(answer)

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
	def answerWh(self, wh, question, sentence):
		answer = ""
		answerLocs = []
		cQuestion = self.clean(question)
		cSentence = self.clean(sentence)
		if (wh == "who"):
			questionEnts = self.ner(cQuestion)
			sentenceEnts = self.ner(cSentence)
			for entNum in range(0,len(sentenceEnts)):
				if (sentenceEnts[entNum][1] == "PERSON"):
					answerLocs.append(entNum)
			answerLocs.append(-1)
			for locNum in range(0,len(answerLocs)-1):
				answer += sentenceEnts[answerLocs[locNum]][0]
				answer += " "
				if (answerLocs[locNum+1] - answerLocs[locNum] > 1):
					answer += "and"
					answer += " "
			if (answer == ""): answer = self.originalSentence # get subject of sentence
			return(answer)
		if (wh == "where"):
			questionEnts = self.ner(cQuestion)
			sentenceEnts = self.ner(cSentence)
			answer = "In "
			for entNum in range(0,len(sentenceEnts)):
				if (sentenceEnts[entNum][1] == "GPE"):
					answerLocs.append(entNum)
			answerLocs.append(-1)
			for locNum in range(0,len(answerLocs)-1):
				answer += sentenceEnts[answerLocs[locNum]][0]
				answer += " "
				if (answerLocs[locNum+1] - answerLocs[locNum] > 1):
					answer += "and"
					answer += " "
			if (answer == ""): answer = sentence # get subject of sentence
			return(answer)
		# time questions
		if (wh == "when"):
			words = cSentence.split()
			answer = ""
			inTimex = 0 # a tracker for if we are in a timex tagged phrase
			for wordNum in range(0,len(words)):
				if (words[wordNum] == "/TIMEX2"):
					inTimex = 0
				if (inTimex == 1):
					answer += words[wordNum]
					answer += " "
				if (words[wordNum] == "TIMEX2"):
					inTimex = 1
			return(answer)
		# what question
		if (wh == "what"):
			answer = sentence # return the whole best sentence

	def run(self):
		# answer all questions
		for i in range(0, len(self.questionList)):
			self.answerQuestion(self.questionList[i], self.sentenceList[i])

if __name__ == '__main__':
	AnsweringMachine(questionDoc=sys.argv[1], sentenceDoc=sys.argv[2]).run()