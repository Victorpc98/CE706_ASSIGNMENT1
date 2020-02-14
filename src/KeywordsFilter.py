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

		tokens = self.remove_stopwords(tokens) # Remove stopwords
		
		# Convert to set so duplicates tokens are delated. Tokens with length equal 1 must be removed.
		vocabulary = { v for v in set(tokens) if len(v) > 1 }
		
		tf = self.termFrequency(vocabulary, documents) # Frequency for each token
		#print(list(tf.items())[0])
		idf = self.inverseDocFrequency(vocabulary, documents)	
		#print(idf)	
		tfidf = self.tf_idf(vocabulary, tf, idf)
		#print(vocabulary)
		#print(list(tfidf.items())[0])
		#print(len(tfidf))
				
		res = []
		
		data = pd.DataFrame({"Words" : sorted(vocabulary)})
		data["IDF"] = [idf[key] for key in sorted(idf.keys())]
		
		docCount = 0
		
		for doc, value in tfidf.items():
		
			sortedList = sorted(value, key=lambda tup: tup[0])
			
			#print(sortedList)
			
			tf_idf_list = []
			
			for token, tf_idf in sortedList:
				tf_idf_list.append(tf_idf)
			
			docCount += 1
			data["doc"+str(docCount)] = tf_idf_list
			

		data.to_csv(OUT_DIR + 'tf_idf.csv')
		
		"""	
		res.append({"Token": t, "TF" : tf[t], "DFT": dft, "IDF" : idf, "TF_IDF" : tf_idf})

		df = pd.DataFrame.from_dict(res,orient='columns') # Convert to dataframe and save to csv
		df = df.set_index('Token')
		df = df.sort_values("TF_IDF",ascending=False)
		df.to_csv(OUT_DIR + 'tf_idf.csv')

		"""
		
		#self.bestKeywords(data)
		#self.bestSentences(data, documents)
		if self.args.verbose: print("\033[K[INFO] Selecting Keywords ... Done")
		
        
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

	def bestKeywords(self, data):
		keywords = data.head(10).index.values.tolist()
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
