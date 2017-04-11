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
		# unpack question and answer from txt files to strings
		with open(questionDoc, 'r') as f:
			questionString = f.read()
			self.originalQuestion = f.read # save copy of original
			questionString = self.clean(questionString)
		self.question = questionString
		with open(sentenceDoc, 'r') as f:
			sentenceString = f.read()
			self.originalSentence = f.read # save copy of original
			sentenceString = self.clean(sentenceString)
		self.sentence = sentenceString
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
		#st = NERTagger('../stanford-ner/classifiers/all.3class.distsim.crf.ser.gz','../stanford-ner/stanford-ner.jar')
		rawEntities = nltk.ne_chunk(nltk.pos_tag(word_tokenize(sentence))).pos() # tree object
		entities = list()
		for ent in rawEntities:
			pureTuple = (ent[0][0], ent[1])
			entities.append(pureTuple)
		return(entities)
>>>>>>> 00efee1aeac3160dc1acf286a12ba0f2e859b4c0

	# input: None
	# output: a STRING, with the part of the sentence bound to contain answer
	# This function is used to obtain noun-based answers when entity-tagging fails
	# used on the sentence conditionally for "who" and always for "what"
	# Works by finding verb, and including words around it
	# def subSentence(self):
	# 	taggedSent = nltk.pos_tag(nltk.word_tokenize(self.originalSentence))
	# 	inPhrase = 0 # switch for when to take words
	# 	NPgrammar = "NP: {<DT>?<JJ>*<NN>}"
	# 	cp = nltk.RegexpParser(NPgrammar)
	# 	result = cp.parse(taggedSent)
	# 	for (wordNum in range(0,taggedSent)):
	# 		if (taggedSent[wordNum][1] in verbTypes):
	# 			verbs.append(wordNum)
	# 		if (taggedSent[wordNum][1] in nounTypes):
	# 			nouns.append(wordNum)
	# 	if (len(verbs) == 0):
	# 		return(self.originalSentence) # no verb... something is wrong
	# 	else:
	# 		first = min(verbs+nouns)
	# 		last = max(verbs+nouns)

	# 	return(subject)

	def answerQuestion(self):
		# st = StanfordPOSTagger('english-bidirectional-distsim.tagger')
		# tags = st.tag('What is the airspeed of an unladen swallow ?'.split())
		#text = pos_tagger.tag(word_tokenize("What's the airspeed of an unladen swallow ?"))
		#print(text)

		# all the question tags we will cownsider
		searchObj = re.findall(r'did|was|is|who|what|where|when|how', self.question, re.I)
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
			answer = self.answerWh(qType.lower())
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
	def answerWh(self, wh):
		answer = ""
		answerLocs = []
		if (wh == "who"):
			questionEnts = self.ner(self.question)
			sentenceEnts = self.ner(self.sentence)
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
			questionEnts = self.ner(self.question)
			sentenceEnts = self.ner(self.sentence)
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
			return(answer)
		# time questions
		if (wh == "when"):
			words = self.sentence.split()
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
			answer = self.originalSentence # return the whole best sentence

	def run(self):
		self.answerQuestion()

if __name__ == '__main__':
	AnsweringMachine(questionDoc=sys.argv[1], sentenceDoc=sys.argv[2]).run()