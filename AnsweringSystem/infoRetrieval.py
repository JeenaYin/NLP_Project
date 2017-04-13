import os, sys
import nltk
from collections import defaultdict
from fuzzywuzzy import fuzz

questionList = []
THRESHOLD = 60


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
	possibleTargetSentences = []
	maxScore = 0
	bestSentence = ""
	for sentence in sentenceList:
		questionRank = fuzz.token_set_ratio(question, sentence)
		#print(sentence)
		#print(questionRank)
		if questionRank > THRESHOLD:
			possibleTargetSentences += [sentence]
		if questionRank > maxScore:
			bestSentence = sentence;
			maxScore = questionRank
	if possibleTargetSentences == []:
		return bestSentence;
	else: 
		#print(possibleTargetSentences)
		return possibleTargetSentences[0]

def answerQuestion(targetSentence):
	return targetSentence

def main():
	questions = getQuestions(sys.argv[1])
	sentenceList = getSentences(sys.argv[2])
	for question in questions:
		target = getTargetSentence(question, sentenceList)
		#print(question)
		#print(target)
	with open("ChosenSentence.txt", "w") as chosen:
		chosen.write(target)
	return 1; 

main();




