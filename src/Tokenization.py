#Victor Perez - vp19885  / 1900232
#Joel Valiente - jv19228 / 1900289

import nltk
from nltk import re
from nltk import word_tokenize
from nltk.stem import WordNetLemmatizer

#Class for computing the tokens given a text.
class Tokenization():

	#Constructor.
	def __init__(self):
		self.lemmatizer = WordNetLemmatizer()

	#Counts the tokens from the given text using the build-in word_tokenize method from ntlk.
	def getTokensNopunct(self, text):

		return [word.lower() for word in word_tokenize(text) if re.search("\w", word)]
