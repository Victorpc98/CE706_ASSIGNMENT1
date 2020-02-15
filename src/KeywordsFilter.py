from nltk import FreqDist
from nltk.corpus import stopwords
from definitions import OUT_DIR
import math
import pandas as pd

class KeywordsFilter():

	def __init__(self,args):
		self.args = args

	def filter(self, tokens, documents):

		if self.args.verbose:
			print("[INFO] Selecting Keywords ...",end="\r",flush=True)
		
		# Convert to set so duplicates tokens are delated. Tokens with length equal 1 must be removed.
		self.vocabulary = { v for v in set(tokens) if len(v) > 1 }
		
		#Some documents are just a letter. Delete them.
		documents = [ d for d in documents if len(d) > 1 ]
		
		tf = self.termFrequency(documents) # Frequency for each token
		idf = self.inverseDocFrequency(documents)	
		tfidf = self.tf_idf(tf, idf)
				
		res = []
		
		data = pd.DataFrame({"Words" : sorted(self.vocabulary)})
		data["IDF"] = [idf[key] for key in sorted(idf.keys())]
		
		for doc, value in tfidf.items():
		
			sortedList = sorted(value, key=lambda tup: tup[0])
			
			tf_idf_list = []
			
			for token, tf_idf in sortedList:
				tf_idf_list.append(tf_idf)
						
			data[doc] = tf_idf_list
			

		data.to_csv(OUT_DIR + 'tf_idf.csv')			
		
		self.bestKeywords(data, idf)
		self.bestSentences(data, documents)
		if self.args.verbose: print("\033[K[INFO] Selecting Keywords ... Done")
		
	def getVocabulary(self):
		
		return self.vocabulary 
        
	def termFrequency(self, documents):
		
		tf_table = {}

		for doc in documents:

			tf_vector = []			

			for token in self.vocabulary:

				#Tuple (token, tf)
				tf_vector.append( (token, doc.count(token)) )

			tf_table[doc] = tf_vector

		return tf_table
	

	# Computes the IDF as [log(N/dft)]. Where N is the # of documents 
	# in the collection and dft is the Document Term Frequency
	def inverseDocFrequency(self, documents):
	
		df_vector = self.documentFrequencyTerm(documents)
		N = len(documents)
		idf_vector = { k: math.log(N/v) for (k,v) in df_vector.items() }

		return idf_vector

	# (DFT) Returns the number of documents where the term appears at
	def documentFrequencyTerm(self, documents):

		df_vector = {}
		
		for token in self.vocabulary:
		
			count = 0

			for doc in documents:				
				if(token in doc):
					count += 1
			
			df_vector[token] = count

		return df_vector

	# Computes tf.idf 
	def tf_idf(self, tf, idf):
		
		tf_idf_table = {}

		for doc, value in tf.items():

			tf_idf_vector = []			
			
			for item in value:
			
				token = item[0]
				tf = item[1]
				
				tf_idf = tf * idf[token]

				tf_idf_vector.append( (token, tf_idf) )

			tf_idf_table[doc] = tf_idf_vector
		
		return tf_idf_table

	# Removes stopwords from the given list of tokens
	def remove_stopwords(self,tokens):
		return [word for word in tokens if word not in stopwords.words('english')]

	def bestKeywords(self, data, idf):		
		
		total_tf_idf = {}
		
		for v in self.vocabulary:
		
			row = data.loc[data["Words"] == v]
			value = row.sum(axis=1).values[0] - idf[v]
			total_tf_idf[v] = value
		
		f = open(OUT_DIR + "best_keywords.txt","w+")
		
		for k, v in sorted(total_tf_idf.items(), key= lambda kv: kv[1], reverse=True):
			f.write(k + " " + str(v) + "\n")
			
		f.close()
		

	def bestSentences(self, data, documents):
	
		
		total_tf_idf = {}
		maxDocCount = len(data.columns)-1

		for doc in documents:
		
			value = data[doc].sum()
			total_tf_idf[doc] = value				
		
		f = open(OUT_DIR + "best_sentences.txt","w+")
		
		for k, v in sorted(total_tf_idf.items(), key= lambda kv: kv[1], reverse=True):
			f.write(k + " -> " + str(v) + "\n")
			
		f.close()
                
#https://stackoverflow.com/a/8272462
#https://stackoverflow.com/a/613218
