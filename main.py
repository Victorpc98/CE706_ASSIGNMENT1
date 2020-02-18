#Victor Perez - vp19885  / 1900232
#Joel Valiente - jv19228 / 1900289

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
from src.Preprocessing import Preprocessing
from src.KeywordsFilter import KeywordsFilter
from src.Pos import POS
from src.Stemming import Stemming

#Main class.
class Main():

	#Constructor.
	def __init__(self):

		#Add the required arguments.
		parser = argparse.ArgumentParser()
		parser.add_argument("-u", "--url", help="Url to parse", default="http://www.multimediaeval.org/mediaeval2019/memorability/")
		parser.add_argument("-v","--verbose", action="store_true", help="Program Verbosity", default=False)
		
		#Parse the given arguments in the command line.
		self.args = parser.parse_args()
		
		#Verbose information shown in the standard output.
		if self.args.verbose: print("[INFO] Initiating execution ...")

		#Create an instance of Parser class.
		self.parser = Parser(self.args)
		#Parse thext from the given url (given in args).
		parsed_text = self.parser.parse()

		#Create an instance of Preprocessing class.
		preprocesser = Preprocessing(self.args)
		#Compute the tokens and the documents after preprocessing the text.
		tokens, documents = preprocesser.process(parsed_text)
		
		#Create an instance of POS class.
		pos = POS(self.args)
		#Compute the PoS tags.
		posTags = pos.tagPosTokens(tokens)

		#Create an instance of KeywordsFilter class.
		keywords_filter = KeywordsFilter(self.args)
		#Compute the TF-IDF table and store the results in files.
		keywords_filter.filter(tokens, documents)
		
		#Returns the vocabulary used for computing TF-IDF table.
		vocabulary = keywords_filter.getVocabulary()
		
		#Create an instance on Stemming class.
		stemming = Stemming(self.args)
		#Stems each word of the vocabulary and store them in a file.
		stemming.stemmVocabulary(vocabulary)


if __name__ == "__main__":
	main = Main()
    
    
"""

References.

https://stackoverflow.com/a/3845449 -> Remove empty strings of a string list.
https://towardsdatascience.com/text-summarization-using-tf-idf-e64a0644ace3  -> tdidf with nltk

"""
