import argparse
"""
Count all the terms and determine the most important terms. Prepositions are NOT important. 
How important is a term?

Inverse Document Frequency ( IDF) : log(N/dft) , where
N : Number of documents in the collection. A collection can be a paragraph, a file, multiple files ...
dft : Number of documents in wich term t appears

Term Frequency (TF) : greater when the term is more frequent
Inverse Term Frequency : greater when the term is rare in the document

TF.IDF = TF * log(N/dtf)

TF.IDF : Accentuates terms that are important in the documents

"""
from src.Parser import Parser
from src.Tokenization import Tokenization
from nltk import FreqDist

class Main():

	def __init__(self):

		parser = argparse.ArgumentParser()
		parser.add_argument("-u", "--url", help="Url to parse",default="http://www.multimediaeval.org/mediaeval2019/memorability/")
		parser.add_argument("-v","--verbose",action="store_true", help="Program Verbosity",default=False)
		self.args = parser.parse_args()
		if self.args.verbose: print("[INFO] Initiating execution ...")

		self.parser = Parser(self.args)
		parsed_text = self.parser.parse()

		#print()
		#print(parsed_text)
		#print()

		print()
		#Split the text in sentences and remove empty strings.
		self.documents = [s.lower() for s in parsed_text.split("\n") if s]
		self.N = len(self.documents)
		
		#print(self.N)
		#print(self.documents)
		#print()

		self.tokenizer = Tokenization()
		tokens = []

		for doc in self.documents:
			
			currentTokens = self.tokenizer.getTokensNopunct(doc)
			tokens.extend(currentTokens)
		
		#print()
		#print(tokens)
		#print()
		#print(len(tokens))
		#print()
		
		posTags = self.tokenizer.tagPosTokens(tokens, "POS")
		
		
		self.tf_idf(tokens)
		

	#Returns a dictionary. Get frequency of an element using freqdist[token]
	def termFrequency(self, tokens):
		
		fdist = FreqDist(tokens)
		
		return fdist
		
	#Returns a dictionary containing all dft.
	def inverseDocFrequency(self, tokens):

		df = {}
		
		
		for t in tokens:
		
			count = 0
			
			for doc in self.documents:
			
				if(t in doc):
					count += 1
				
			df[t] = count
		
		return df
		
	def tf_idf(self, tokens):

		result = {}
		
		tf = self.termFrequency(tokens)
		df = self.inverseDocFrequency(tokens)
		
		print(tf["mediaeval"])
		print(df["mediaeval"])


if __name__ == "__main__":
	main = Main()
    
    
"""

https://stackoverflow.com/a/3845449 -> Remove empty strings of a string list.
https://towardsdatascience.com/text-summarization-using-tf-idf-e64a0644ace3  -> tdidf with nltk

"""
