from nltk import FreqDist
from nltk.corpus import stopwords
from definitions import OUT_DIR
import math
#import pandas as pd

class KeywordsFilter():

	def __init__(self,args):
		self.args = args

	def filter(self, tokens, documents):

		if self.args.verbose:
			print("[INFO] Selecting Keywords ...",end="\r",flush=True)

		tokens = self.remove_stopwords(tokens) # Remove stopwords
		
		# Convert to set so duplicates tokens are delated
		vocabulary = set(tokens)
		
		tf = self.termFrequency(vocabulary, documents) # Frequency for each token
		print(list(tf.items())[0])
		idf = self.inverseDocFrequency(vocabulary, documents)
		
		tfidf = self.tf_idf(vocabulary, tf, idf)
		
		res = []
		"""
		for t in tokens: # for each token compute dft, idf and tf_idf
			dft = self.documentFrequencyTerm(t,documents)
			idf = self.inverseDocFrequency(dft,t,documents)
			tf_idf = self.tfIdf(tf[t],idf)
			res.append({"Token": t, "TF" : tf[t], "DFT": dft, "IDF" : idf, "TF_IDF" : tf_idf})

		df = pd.DataFrame.from_dict(res,orient='columns') # Convert to dataframe and save to csv
		df = df.set_index('Token')
		df = df.sort_values("TF_IDF",ascending=False)
		df.to_csv(OUT_DIR + 'tf_idf.csv')

		self.bestKeywords(df)
		self.bestSentences(df,documents)
		if self.args.verbose: print("\033[K[INFO] Selecting Keywords ... Done")
		"""
        
	def termFrequency(self, vocabulary, documents):
		
		tf_table = {}

		for doc in documents:

			tf_vector = []

			for token in vocabulary:

				#Tuple (token, tf)
				tf_vector.append( (token, doc.count(token)) )

			tf_table[doc] = tf_vector


		return tf_table
	

	# Computes the IDF as [log(N/dft)]. Where N is the # of documents 
	# in the collection and dft is the Document Term Frequency
	def inverseDocFrequency(self, vocabulary, documents):
	
		df_vector = self.documentFrequencyTerm(vocabulary, documents)
		N = len(documents)
		idf_vector = { k: math.log(N/v) for (k,v) in df_vector.items() }

		return idf_vector

	# (DFT) Returns the number of documents where the term appears at
	def documentFrequencyTerm(self, vocabulary, documents):

		df_vector = {}
		
		for token in vocabulary:
		
			count = 0

			for doc in documents:
				if(token in doc):
					count += 1
			
			df_vector[token] = count

		return df_vector

	# Computes tf.idf 
	def tf_idf(self, vocabulary, tf, idf):
		
		tf_idf_table = {}

		for (doc,value) in tf:

			tf_idf_vector = []
			
			for item in value:
			
				token = item[0]
				tf = item[1]
				
				tf_idf = tf * idf[token]

				tf_vector.append( (token, tf_idf) )

			tf_table[doc] = tf_vector

	# Removes stopwords from the given list of tokens
	def remove_stopwords(self,tokens):
		return [word for word in tokens if word not in stopwords.words('english')]

	def bestKeywords(self,df):
		keywords = df.head(10).index.values.tolist()
		with open(OUT_DIR + "best_keywords.txt","w+") as f:
			f.write("\n".join(keywords))

	def bestSentences(self,df,documents):
		words = df.index.values.tolist()
		res = []
		for doc in documents:
			avg = 0
			for w in words:
				if w in doc:
				    avg += df.iloc[df.index == w].IDF[0]
			res.append({"Document" : doc, "Importance" : avg})

		a = pd.DataFrame.from_dict(res,orient='columns')
		a.set_index("Document")
		a = a.sort_values("Importance",ascending=False)
		a.to_csv(OUT_DIR + 'best_sentences.csv',index=False)

                
#https://stackoverflow.com/a/8272462
