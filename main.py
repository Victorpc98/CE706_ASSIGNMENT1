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

class Main():

    def __init__(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("-u", "--url", help="Url to parse",default="http://www.multimediaeval.org/mediaeval2019/memorability/")
        parser.add_argument("-v","--verbose",action="store_true", help="Program Verbosity",default=False)
        self.args = parser.parse_args()
        if self.args.verbose: print("[INFO] Initiating execution ...")

        self.parser = Parser(self.args)
        parsed_text = self.parser.parse()

    def execute(self):
        pass


if __name__ == "__main__":
    main = Main()