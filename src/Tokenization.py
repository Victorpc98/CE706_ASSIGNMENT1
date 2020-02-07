import nltk
from nltk import re
from nltk import word_tokenize
from nltk.stem import WordNetLemmatizer
from src.assignment1.UrlDownloader import URLDownloader

class Tokenization():
	"""
	This class solves the Part 1 Exercises.
	"""
	def __init__(self):
		self.url_target = "https://www.theguardian.com/music/2018/oct/19/while-my-guitar-gently-weeps-beatles-george-harrison"
		self.lemmatizer = WordNetLemmatizer()

	def getText(self):
		"""
		Gets the text contained inside the <p></p> tags from the given url_target. Removes the links and returns a string
		of all the p tags found.
		"""

		url = URLDownloader()
		html = url.getPlainHtml(self.url_target)
		text = re.findall("<p>(.*?)<\/p>", html)
		result = ' '.join(text)
		result = self.removeLinks(result)

		return result

	def getTokensNopunct(self, text):
		"""
		Counts the tokens from the given text by using the build-in word_tokenize method from the ntlk package
		"""

		return [word.lower() for word in word_tokenize(text) if re.search("\w", word)]

	def getTypesNopunct(self, text):
		"""
		Counts the types from the given text the same way as getTokensNopunct() but now, making the output list
		unique by converting it to a set.
		"""

		return set([word.lower() for word in word_tokenize(text) if re.search("\w", word)])
		
	def removeLinks(self, text):
		"""
		Removes the links from the given text by using a regex to substitute them for nothing
		"""
	
		return re.sub(r'<.*?>', '', text)
		
	def getTokensNopunctAfterLemmatization(self, text):
		"""
		Returns the tokens from the given text after applying lemmatization. It uses the built-in Lemmatizer from 
		the nltk package
		"""
	
		tokensNopunct = self.getTokensNopunct(text)
		
		return [self.lemmatizer.lemmatize(word) for word in tokensNopunct]
		
	def getTypesNopunctAfterLemmatization(self, text):
		"""
		Returns the types from the given text after lemmatization. Works the same way as getTypesNopunctAfterLemmatization,
		but it returns a unique list of words by converting it to a set.
		"""
	
		typesNopunct = self.getTypesNopunct(text)
		
		return set([self.lemmatizer.lemmatize(word) for word in typesNopunct])
		
	def tagPosTokens(self, tokens, outputName):
		"""
		Computes the POS Tags for every token in the tokens list and stores this information in
		the /output folder.
		"""

		if(".txt" not in outputName):
			outputName += ".txt"
			
		tags = nltk.pos_tag(tokens)
			
		with open("output/" + outputName, 'w+') as f:
			for item in tags:
				f.write(str(item) + "\n")
        
		return tags

""" 
References :
	findall: https://developers.google.com/edu/python/regular-expressions
	regex <p></p>: https://stackoverflow.com/questions/46080740/regex-to-extract-pure-text-within-specific-html-tag
	string from a list: https://stackoverflow.com/questions/5618878/how-to-convert-list-to-string
	clean html tags: https://medium.com/@jorlugaqui/how-to-strip-html-tags-from-a-string-in-python-7cb81a2bbf44
	re.sub examples: https://lzone.de/examples/Python%20re.sub
	Lemmatization: https://www.geeksforgeeks.org/python-lemmatization-with-nltk/
	POS tagger: https://www.nltk.org/book/ch05.html
	taggs in a file: https://stackoverflow.com/questions/899103/writing-a-list-to-a-file-with-python
"""