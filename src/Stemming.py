#Victor Perez - vp19885  / 1900232
#Joel Valiente - jv19228 / 1900289

from definitions import OUT_DIR
import nltk
from nltk import re
from nltk import word_tokenize
from nltk.stem import WordNetLemmatizer

#Class for stemming the vocabulary words.
class Stemming():
	
	#Constructor
	def __init__(self,args):

		self.args = args
		
		#Class from nltk for stemming words.
		self.lemmatizer = WordNetLemmatizer()
		
	#Writes the stems of the words belonging to the vocabulary.
	def stemmVocabulary(self, vocabulary):
		
		#Compute the stems given the vocabulary.		
		vocLemma =  [self.lemmatizer.lemmatize(word) for word in vocabulary]
		
		#Write them in a file.
		with open(OUT_DIR + "tokensAfterStemming.txt","w+") as f:
			for i in vocLemma:
				f.write(i + "\n")
