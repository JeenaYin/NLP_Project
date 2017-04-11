import os 
import en
import nltk
from nltk.parse import stanford
from nltk import word_tokenize, pos_tag
from nltk.tag.stanford import StanfordNERTagger
import re

directory = "/Users/charisseharuta/Documents/CMU/Spring2017/NLP/" 
# "/Users/sumedhamehta/StanfordTools/"

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
		

def who(sentence):
	possQs = []
	for i in range(0, sentence.len):
		if sentence.ner[i][1] == 'PERSON':
			possQs.append("Who is " + sentence.ner[i][0])
		else:
			if en.is_verb(sentence.tokenized[i]):
				possQs.append("Who " + str(sentence.tokenized[0:]))

	return possQs


def when(sentence):
	for i in range(0, sentence.len):
		if sentence.when[i][1] == 'DATE':
			return ("When do " + str(sentence.tokenized[0:i - 1]))



#testing
sentences = "George is the president of the united states of america"

testSent = Sentences(sentences)

test0 = Sentence(testSent, 0)
# test1 = Sentence(testSent, 1)
# test2 = Sentence(testSent, 2)
# test3 = Sentence(testSent, 3)


print(who(test0))
# print(who(test1))
# print(who(test2))
# print(who(test3))

# print(when(test0))
# print(when(test1))
# print(when(test2))
# print(when(test3))

