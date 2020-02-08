from src.Tokenization import Tokenization
import itertools
from definitions import OUT_DIR
import re
class Preprocessing():

	def __init__(self,args):
		self.args = args
		self.tokenizer = Tokenization()

	def process(self,text):
		if self.args.verbose: print("[INFO] Pre-processing HTML ...",end="\r",flush=True)
		documents = [s.lower() for s in re.split(r'\n|\.',text) if s]
		print(documents)
		N = len(documents)

		tokens = list(itertools.chain.from_iterable([ self.tokenizer.getTokensNopunct(doc) for doc in documents]))
		with open(OUT_DIR + "preprocessing.txt","w+") as f:
			for i in tokens:
				f.write(i + "\n")

		if self.args.verbose: print("\033[K[INFO] Pre-processing HTML ... Done")
		return tokens,documents
