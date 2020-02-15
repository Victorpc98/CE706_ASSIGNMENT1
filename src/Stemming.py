from definitions import OUT_DIR
import nltk
from nltk import re
from nltk import word_tokenize
from nltk.stem import WordNetLemmatizer

class Stemming():
	"""
	This class solves the Part 1 Exercises.
	"""
	def __init__(self,args):
		self.args = args
		self.lemmatizer = WordNetLemmatizer()
		
	def stemmVocabulary(self, vocabulary):
		"""
		Returns the given tokens applying lemmatization. It uses the built-in Lemmatizer from 
		the nltk package
		"""
		
		vocLemma =  [self.lemmatizer.lemmatize(word) for word in vocabulary]
		
		with open(OUT_DIR + "tokensAfterStemming.txt","w+") as f:
			for i in vocLemma:
				f.write(i + "\n")
