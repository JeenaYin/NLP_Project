import os
import nltk
from collections import defaultdict
from fuzzywuzzy import fuzz

questionList = []
questionRanks = dict()
THRESHHOLD = 50


def getQuestions(questionfile):
	with open(questionfile, "rt") as fileContents:
		content = fileContents.read()
		fileContents.close()

	for question in content.splitlines():
		questionList.append(question)


	return questionList

def getSentences(textfile):
	with open(textfile, "rt") as fileContents:
		content = fileContents.read()
		fileContents.close()

	possibleSentences = nltk.tokenize.sent_tokenize(content)
	return possibleSentences


def getTargetSentence(question, sentenceList):
	questionDict = dict()
	maxScore = 0
	bestSentence = ""
	for sentence in sentenceList: 
		questionRank = fuzz.partial_ratio(question, sentence)
		if questionRank > maxScore:
			bestSentence = sentence;
			maxScore = questionRank
	return bestSentence;

def answerQuestion(targetSentence):
	return targetSentence

def main():
	questions = getQuestions("SampleQuestion.txt")
	sentenceList = getSentences("SampleDocument.txt")
	for question in questions:
		target = getTargetSentence(question, sentenceList)
		print(question)
		print(target)
	return 1; 

main();


# things to change, depending on the type of sentence. choose target sentence accordingly, 
# output sever sentences and use them to further determine certain types of question.



