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

class Main():

	def __init__(self):

		parser = argparse.ArgumentParser()
		parser.add_argument("-u", "--url", help="Url to parse",default="http://www.multimediaeval.org/mediaeval2019/memorability/")
		parser.add_argument("-v","--verbose",action="store_true", help="Program Verbosity",default=False)
		self.args = parser.parse_args()
		if self.args.verbose: print("[INFO] Initiating execution ...")

		self.parser = Parser(self.args)
		parsed_text = self.parser.parse()

		preprocesser = Preprocessing(self.args)
		tokens,documents = preprocesser.process(parsed_text)

		pos = POS(self.args)
		posTags = pos.tagPosTokens(tokens)

		keywords_filter = KeywordsFilter(self.args)
		keywords_filter.filter(tokens,documents)


if __name__ == "__main__":
	main = Main()
    
    
"""

https://stackoverflow.com/a/3845449 -> Remove empty strings of a string list.
https://towardsdatascience.com/text-summarization-using-tf-idf-e64a0644ace3  -> tdidf with nltk

"""
