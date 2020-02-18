#Victor Perez - vp19885  / 1900232
#Joel Valiente - jv19228 / 1900289

from src.Tokenization import Tokenization
import itertools
from definitions import OUT_DIR
import re
from nltk.corpus import stopwords

#Class for preprocessing the text.
class Preprocessing():

	#Constructor.
	def __init__(self,args):
		self.args = args
		self.tokenizer = Tokenization()

	#Preprocess the given text.
	def process(self,text):
	
		if self.args.verbose: print("[INFO] Pre-processing HTML ...",end="\r",flush=True)
		
		#Split the text given a new line or a dot.
		initialDocuments = [s.lower() for s in re.split(r'\n|\.',text) if s]
		
		#Initialize the documents list.
		documents = []
		
		#For each document in intial documents list.
		for doc in initialDocuments:
			
			#Get the tokens of the current document.
			docTokens = self.tokenizer.getTokensNopunct(doc)
			#Remove the stopwords belonging in the current document.
			docTokens = self.remove_stopwords(docTokens)
			#Appends all the valid tokens as the final document.
			documents.append(" ".join(docTokens))

		#Total number of documents of our corpus.
		N = len(documents)

		#Compute the tokens given the documents.
		tokens = list(itertools.chain.from_iterable([ self.tokenizer.getTokensNopunct(doc) for doc in documents]))
		
		#Store the tokens in a txt file.
		with open(OUT_DIR + "preprocessing.txt","w+") as f:
			for i in tokens:
				f.write(i + "\n")

		if self.args.verbose: print("\033[K[INFO] Pre-processing HTML ... Done")
		
		#Return both the tokens and the documents.
		return tokens,documents
		
	#Removes stopwords from the given list of tokens
	def remove_stopwords(self, tokens):
		return [word for word in tokens if word not in stopwords.words('english')]
