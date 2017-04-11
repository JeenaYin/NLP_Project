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


# def getParse(sentences):
# 	os.environ['CLASSPATH'] = directory+'stanford-parser-full-2015-04-20'
#     os.environ['STANFORD_PARSER'] = directory+'stanford-parser-full-2015-04-20/stanford-parser.jar'
#     os.environ['STANFORD_MODELS'] = directory+'stanford-parser-full-2015-04-20/stanford-parser-3.6.0-models.jar'
#     p = stanford.StanfordParser(model_path=directory+"stanford-parser-full-2015-04-20/models/edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz")
#     iterTrees = p.raw_parse_sents(sentences)
#     treeList = []
#     for i in iterTrees:
#     	for t in i:
#     		treeList.append(tree)
#    	return treeList


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


 # def getWhereQuestions(s):
 # 	n = s.NER
 # 	p = s.pos
 # 	nerTags = copy.deepcopy(n)
 # 	sentence = s.tokenized
 # 	posTags = copy.deepcopy(n)
 	







# def getHowQuestions(s):

#testing
sentences = "Bob is really nice and really cool."
testSent = Sentences(sentences)
testS = Sentence(testSent, 0)
print(getBinaryQuestions(testS))



