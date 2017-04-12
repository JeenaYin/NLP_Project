import os 
import nltk
import en
from nltk.parse import stanford
from nltk import word_tokenize, pos_tag
from nltk.tag.stanford import StanfordNERTagger
import re
import copy



#charisse: who what when why
#sumi: binary, how, where

directory = "/Users/sumedhamehta/StanfordTools/" #"/Users/charisseharuta/Documents/CMU/Spring2017/NLP/" 

class Sentences:
	def __init__(self, content):

		raw = content.strip()
		self.pronoun = getProN(raw)
		self.sentences = nltk.tokenize.sent_tokenize(content)
		self.size = len(self.sentences)
		tokenizedSentences = []
		for s in self.sentences:
			tokenizedSentences.append(word_tokenize(s))
		self.tokenized = tokenizedSentences

		self.ner = getNER(self.tokenized)
		self.when = getWhen(self.tokenized)
		self.pos = getPOS(self.tokenized)



def getProN(raw):
	pNounCounts = dict()
	tokenized = word_tokenize(raw)
	os.environ['CLASSPATH'] = directory+"stanford-ner-2015-04-20"
	ner_tags = StanfordNERTagger(directory+"stanford-ner-2015-04-20/classifiers/english.all.3class.distsim.crf.ser.gz").tag(tokenized)
	for (w, t) in ner_tags:
		# words are represented as (word, tag)
		if t == "PERSON":
			if(w not in pNounCounts):
				pNounCounts[w] = 1
			else:
				pNounCounts[w] +=1
	maxWord = "";
	maxCount = 0;
	for k in pNounCounts:
		if maxCount < pNounCounts[k]:
			maxCount = pNounCounts[k]
			maxWord = k
	# print(maxWord)
	return maxWord


def getNER(tokenizedSentences):
	os.environ['CLASSPATH'] = directory+"stanford-ner-2015-04-20"
	nerTags = StanfordNERTagger(directory+'stanford-ner-2015-04-20/classifiers/english.all.3class.distsim.crf.ser.gz').tag_sents(tokenizedSentences)
	# print(nerTags)
	return nerTags

def getWhen(tokenizedSentences):
	os.environ['CLASSPATH'] = directory+"stanford-ner-2015-04-20"
	whenTags = StanfordNERTagger(directory+'stanford-ner-2015-04-20/classifiers/english.muc.7class.distsim.crf.ser.gz').tag_sents(tokenizedSentences)
	# print(whenTags)
	return whenTags

def getPOS(tokenizedSentences):
	posTags = []
	for s in tokenizedSentences:
		posTags.append(pos_tag(s))
	# print(posTags)
	return posTags

class Sentence:

	def __init__(self, s, n):
		self.currSent = s.sentences[n]
		self.tokenized = s.tokenized[n]
		self.ner = s.ner[n]
		self.when = s.when[n]
		self.pos = s.pos[n]
		self.pronoun = s.pronoun
		

def getBinaryQuestions(s):
	posTag = copy.deepcopy(s.pos)
	pronoun = s.pronoun
	change = False
	possibleBeginnings = {"is", "are", "does", "were", "can", "were", "will", "has", "had", "have", "could", "would", "should"}
	possVerbs = []
	for i in range(len(posTag)):
		word = posTag[i][0]
		tag = posTag[i][1]
		if word in possibleBeginnings: 
			possVerbs.append(i)

	print(possVerbs)
	if len(possVerbs) == 0:
		posTag.insert(0, ('did', 'VBD')) #verb past tense
		change = True
	else:
		posTag.insert(0, posTag.pop(possVerbs[0]))


	if posTag[1][1] == "NNP" or posTag[1][1] == "DT":
		proper = True
	else: 
		proper = False
	
	finalQ = posTag[0][0].title() + " "
	print(posTag)
	for i in range(len(posTag)-1):
		w = posTag[i+1][0]
		if i == 0:
			if posTag[1][1] == "PRP":
				print(pronoun)
				w = pronoun
			elif posTag[1][1] == "NNP":
				print(word)
				w = w.lower()

		if i == len(posTag)-2:
			if (posTag[i+1][0] in {".", "!"}):
				w = '?'

		wnew = ""
		if change:
			try: 
				wnew = en.verb.present(w)

			except: 
				wnew = w

		else:
			wnew = w

		if i == len(posTag)-3:
			finalQ += wnew

		else:
			finalQ += wnew + ' '

	return [finalQ]


def getWhereQuestions(s):
 	n = s.ner
 	p = s.pos
 	nerTag = copy.deepcopy(n)
 	sentence = s.tokenized
 	posTag = copy.deepcopy(p)
 	finalQ = []
 	subjectFirst = False
 	locationFirst = False
 	subjectFirstIndex = 0 
 	locationFirstIndex = 0
 	vals = dict()

 	for w in range(len(sentence)):
 		if subjectFirst:
 			if (posTag[w][1] in {"VBD", "VBZ"}):
 				vals["verb"] = (sentence[w], w)


 			if (nerTag[w][1] == "LOCATION" and sentence[w-1] in {"at", "in"}):
 				subjectFirstIndex = w - 1 #ending
  		
  		if locationFirst: 
  			if (posTag[w][1] in {"VBD", "VBZ"}):
  				vals["verb"] = (sentence[w], w)
  				locationFirstIndex = w  #starting
  				break


 		if(not subjectFirst and not locationFirst): 
 			if(nerTag[w][1] == "LOCATION"):
 				locationFirst = True 
 			elif(posTag[w][1] in {"NN", "NNP", "PRP"}):
 				subjectFirst = True
 				vals["sub"] = (sentence[w], w)

 	if subjectFirstIndex == 0 and locationFirstIndex == 0:
 		return []

 	elif subjectFirst:
 		w1 = vals["verb"][1]
 		bigchunk1 = ''.join(str(e) for e in sentence[w1+1:subjectFirstIndex])
 		bigchunk1 = bigchunk1.replace(",", " ")

 		w0 = vals["sub"][1]
 		bigchunk0 = ''.join(str(e) for e in sentence[w0-1:w1])
 		print(bigchunk0)
 		bigchunk0 = bigchunk0.replace(",", " ")
 		if (vals["verb"][0] in {"is", "was"}):
 			return ["Where " + vals["verb"][0]+ " " + bigchunk0 + " " + bigchunk1 + "?"]
 		elif(nerTag[vals["verb"][1]][1] == "VBD"):
 			return ["Where did " + vals["sub"][0] + en.verb.present(vals["verb"][0])+ " " + bigchunk1 + "?"]
 		else:
 			return ["Where does " + vals["sub"][0] +  en.verb.present(vals["verb"][0])+ " " + bigchunk1 + "?"]

 	elif locationFirst:
 		w = vals["verb"][1]

 		bigchunk = ''.join(str(e) + " " for e in sentence[locationFirstIndex:])
 		bigchunk = bigchunk.replace(".", "")
 		bigchunk = bigchunk.replace("!", "")
 		return["Where is " + bigchunk + "?"]

 	else:
 		return []


def getWhyQuestions(s):
	n = s.ner
 	p = s.pos
 	nerTag = copy.deepcopy(n)
 	sentence = s.tokenized
 	posTag = copy.deepcopy(p)
 	verbType = None
 	possible = False
 	verbSeen = False
 	subjectSeen = False
 	becauseSynonyms = {"because", "since"}
 	verbI = None
 	subI = None
 	end = 0
 	dt = None
 	print(posTag)
 	for word in becauseSynonyms:
 		if word in sentence:
 			possible = True

 	if not possible: 
 		return []
 	for w in range(len(sentence)):
 		print(sentence[w])
 		if sentence[w] in {"because", "since"}:
 			end = w
 		if posTag[w][1] in {"NN", "NNP", "PRP", "NNS"} and not subjectSeen:
 			subI = w
 			print(subI)
 			subjectSeen = True
 			if(w-1 >= 0):
 				if(posTag[w-1][1] == "DT"):
 					dt = sentence[w-1]
 				else:
 					dt = None

 		if posTag[w][1] in {"VBD", "VBZ", "VBP"} and not verbSeen:
 			verbSeen = True
 			verbI = w

 	print(subI)

 	if subI != None and verbI!=None:
 		bigchunk = ''.join(str(e) + " " for e in sentence[verbI+1:end])
 		bigchunk = bigchunk.replace(".", "")
 		bigchunk = bigchunk.replace("!", "")
 		if dt == None: 
 			return ["Why" + " " + sentence[verbI] + " " + sentence[subI] + " " + bigchunk + "?"]
 		else:
 			return ["Why" + " " + sentence[verbI] + " " + dt + " " + sentence[subI] + " " + bigchunk + "?"]


# def getHowQuestions(s):

#testing
sentences = "Pandas are becoming extinct because they don't give birth to that many babies."
testSent = Sentences(sentences)
testS = Sentence(testSent, 0)
print(getWhyQuestions(testS))



