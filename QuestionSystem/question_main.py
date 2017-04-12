import os 
# import en
import nltk
from nltk.parse import stanford
from nltk import word_tokenize, pos_tag
from nltk.tag.stanford import StanfordNERTagger
import re
import copy



#charisse: who what when why
#sumi: binary, how, where

directory =  "/Users/charisseharuta/Documents/CMU/Spring2017/NLP/"  #"/Users/sumedhamehta/StanfordTools/" 

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
		
		self.len = len(self.tokenized)

	def __repr__(self):
		return str(self.ner)
		


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

#testing

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
 	

def who(sentence):
	q = []
	found = False
	newSubject = False
	persons = 0
	for i in range(0, sentence.len):
		if found:
			if (sentence.pos[i][1] in ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ', 'MD'] 
				and sentence.ner[i-1][1] in ['PERSON', 'ORGANIZATION']):
				q.pop()
				q.append("Who")
				q.append(sentence.tokenized[i])
				newSubject = True
			else:
				q.append(sentence.tokenized[i])
		if not found and sentence.pos[i][1] in ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ', 'MD'] and i != 0:
			q.append("Who")
			q.append(sentence.tokenized[i])
			found = True
		if i == sentence.len - 1:
			q.pop()
			q.append("?")

	return q


def when(sentence):
	q = []
	found = False
	for i in range(1, sentence.len):
		if not found:
			if ((sentence.ner[i-1][1] == 'PERSON' and i < sentence.len - 1) and 
			   ((sentence.pos[i][1] == 'MD' and sentence.pos[i+1][1] == 'VB') or
			    (sentence.pos[i][1] == 'VBD' and sentence.pos[i+1][1] == 'VBG'))):
				q.append("When")
				q.append(sentence.tokenized[i])
				q.append(sentence.tokenized[i-1])
				found = True

			else:
				if (sentence.ner[i-1][1] == 'PERSON' and i < sentence.len and
					(sentence.pos[i][1] in ['VBZ', 'VBD'])):
					if sentence.pos[i][1] == 'VBZ':
						verb = "will"
					else:
						verb = "did"
					new = sentence.tokenized[i]
					q.append("When")
					q.append(verb)
					q.append(sentence.tokenized[i-1])
					q.append(new)
					found = True

		else:
			if (sentence.when[i][1] in ['DATE', 'TIME'] or sentence.tokenized[i]
				in ['today', 'tomorrow', 'yesterday']):
				if sentence.tokenized[i-1] in ["by", "after", "before", "during", "when", "while", 'on', 'in', 'last']:
					q.pop()
				q.append("?")
				return q
			elif (sentence.tokenized[i] in ["after", "before", "during", "when", "while"]):
				q.append("?")
				return q
			elif i != sentence.len - 1:
				q.append(sentence.tokenized[i])
			else:
				return q


def what(sentence):
	q = []
	found = False
	for i in range(1, sentence.len):
		if i == sentence.len - 1:
			if len(q) != 0:\
				q.append("?")
			return q
		if found:
			if sentence.pos[i][1] in ['NN', 'NNP', 'NNS', 'PRP'] and sentence.tokenized[i-1] == 'and':
				q.pop()
				q.append("?")
				return q
			q.append(sentence.tokenized[i])
		if (sentence.pos[i][1] in ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ', 'MD']
			and sentence.ner[i-1][1] != 'PERSON' and sentence.pos[i-1][1] in 
			['NN', 'NNP', 'NNS', 'PRP'] and not found):
			q.append("What")
			q.append(sentence.tokenized[i])
			found = True



