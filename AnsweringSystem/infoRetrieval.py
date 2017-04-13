import os, sys
import nltk
import string
from nltk.stem.wordnet import WordNetLemmatizer
from collections import defaultdict
from fuzzywuzzy import fuzz

questionList = []
THRESHOLD = 60
wnl = WordNetLemmatizer()

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

# Take a sentence and return its stripped down, lemmatized form
def lemmatize(s):
	# remove punctuation
	translator = str.maketrans('', '', string.punctuation)
	s2 = s.translate(translator)
	lemString = ""
	for word in s2.split():
		lemString += wnl.lemmatize(word.lower())
		lemString += " "
	return lemString


def getTargetSentence(question, sentenceList):
	questionDict = dict()
	possibleTargetSentences = []
	maxScore = 0
	bestSentence = ""
	lemQuestion = lemmatize(question)
	for sentence in sentenceList:
		lemSentence = lemmatize(sentence)
		questionRank = fuzz.token_set_ratio(lemQuestion, lemSentence)
		print(sentence)
		print(questionRank)
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
	with open("ChosenSentences.txt", "w") as chosen:
		chosen.write("")
	for question in questions:
		target = getTargetSentence(question, sentenceList)
		#print(question)
		#print(target)
		with open("ChosenSentences.txt", "a") as chosen:
			chosen.write(target)
			chosen.write("\n")
	return 1; 

main();




