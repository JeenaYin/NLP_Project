import os 
import nltk
from nltk.parse import stanford
from nltk import word_tokenize, pos_tag
from nltk.tag.stanford import StanfordNERTagger
import re


#my directory where all my stanford things are stored
# directory = "/Users/sumedhamehta/StanfordTools/"
directory = "/Users/charisseharuta/Documents/CMU/Spring2017/NLP/" 
# "/Users/sumedhamehta/StanfordTools/"


class Sentences:
	def __init__(self, content):


		
		raw = content.strip()  #content.strip().decode("ascii", "ignore").encode("ascii")
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


#get pronoun of the text 
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

#get all named entitites for everything
def getNER(tokenizedSentences):
	os.environ['CLASSPATH'] = directory+"stanford-ner-2015-04-20"
	nerTags = StanfordNERTagger(directory+'stanford-ner-2015-04-20/classifiers/english.all.3class.distsim.crf.ser.gz').tag_sents(tokenizedSentences)
	# print(nerTags)
	return nerTags


#get all when tags
def getWhen(tokenizedSentences):
	os.environ['CLASSPATH'] = directory+"stanford-ner-2015-04-20"
	whenTags = StanfordNERTagger(directory+'stanford-ner-2015-04-20/classifiers/english.muc.7class.distsim.crf.ser.gz').tag_sents(tokenizedSentences)
	print(whenTags)
	return whenTags


#get all parts of speech
def getPOS(tokenizedSentences):
	posTags = []
	for s in tokenizedSentences:
		posTags.append(pos_tag(s))
	# print(posTags)
	return posTags




#testing
sentences = "I like Sarah on May 14th"

testSent = Sentences(sentences)





