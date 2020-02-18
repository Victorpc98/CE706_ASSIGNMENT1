#Victor Perez - vp19885  / 1900232
#Joel Valiente - jv19228 / 1900289

from nltk import FreqDist
from nltk.corpus import stopwords
from definitions import OUT_DIR
import math
import pandas as pd

#Class for selecting the keywords.
class KeywordsFilter():

	#Constructor.
	def __init__(self,args):
		self.args = args

	#Main function. This function computes performs the weighting step.
	def filter(self, tokens, documents):

		if self.args.verbose:
			print("[INFO] Selecting Keywords ...",end="\r",flush=True)
		
		#Creates the vocabulary (unique words) given the tokens. Tokens of length equal 1 are removed.
		self.vocabulary = { v for v in set(tokens) if len(v) > 1 }
		
		#Some documents are just a letter. Delete them.
		documents = [ d for d in documents if len(d) > 1 ]
		
		tf = self.termFrequency(documents)			#Compute the term frequency for all documents.
		idf = self.inverseDocFrequency(documents)	#Computes the idf for all tokens in vocabulary.
		tfidf = self.tf_idf(tf, idf)				#Computes the tf-idf table. 

		#Creates a pandas' dataFrame to write the results in a csv file.
		#The first column contains the vocabulary alphabetical sorted.
		data = pd.DataFrame({"Words" : sorted(self.vocabulary)})
		
		#The second column contains the idf of each word in the vocabulary. Idf dictionary is sorted
		#in order to correctly match each word with its idf value.
		data["IDF"] = [idf[key] for key in sorted(idf.keys())]
		
		#For each document belonging to the tf-idf table.
		for doc, value in tfidf.items():
		
			#Sort the list of tuples (word, tf-idf)
			sortedList = sorted(value, key=lambda tup: tup[0])
			
			tf_idf_list = []
			
			#For each element in the previous tuple list.
			for token, tf_idf in sortedList:
				tf_idf_list.append(tf_idf)	#Store each value in a temporal list.

			#Creates a column with the document as the title and the tf-idf values for that document
			#as the column values.
			data[doc] = tf_idf_list
			
		#Write the dataFrame to a csv file.
		data.to_csv(OUT_DIR + 'tf_idf.csv')			
		
		#Rank the vocabulary words in descending order.
		self.bestKeywords(data, idf)
		
		#Rank the documents in descending order.
		self.bestSentences(data, documents)
		
		if self.args.verbose: print("\033[K[INFO] Selecting Keywords ... Done")
		
	#Returns the vocabulary. Used in the main by Stemming class.
	def getVocabulary(self):
		
		return self.vocabulary 
        
    #Compute the term frequency vector for each document (tf table).
	def termFrequency(self, documents):
		
		#Table containing for each document the term frequency (space vector) as list of tuples
		#(word, term frequency for the current document).
		tf_table = {}

		for doc in documents:

			tf_vector = []		#Initialize the list of tuples.		

			#For each word in vocabulary.
			for token in self.vocabulary:

				#Compute the times a word appears in the document and create the tuple (token, tf).
				tf_vector.append( (token, doc.count(token)) )

			#Store in the table (dictionary) the vector space for that document.
			tf_table[doc] = tf_vector

		#Return the term frequency table.
		return tf_table
	

	#Computes the IDF as [log(N/dft)] where N is the # of documents 
	#in the collection and dft is the Document Term Frequency.
	def inverseDocFrequency(self, documents):
		
		#Compute the document frequency.
		df_vector = self.documentFrequencyTerm(documents)
		
		#Compute the number of documents.
		N = len(documents)
		
		#Compute the dictionary of idf. The key is the word in the vocabulary and the
		#value is the idf for that word.
		idf_dict = { k: math.log(N/v) for (k,v) in df_vector.items() }

		#Return the idf dictionary.
		return idf_dict

	#Computes the number of documents where each term of the vocabulary appears on.
	def documentFrequencyTerm(self, documents):

		#Initialize the dictionary containing as key the word of the vocabulary and as value
		#the document fequency of that term.
		df_vector = {}
		
		#For each word of the vocabulary
		for token in self.vocabulary:
		
			count = 0
			
			#For each document.
			for doc in documents:
				
				#If the word appears on that document increaase the counter by one.			
				if(token in doc):
					count += 1
			
			#Add to the dictionary these new values.
			df_vector[token] = count

		#Return the dt.
		return df_vector

	#Computes the tf-idf table. The key is the document and the value is a tuple list as
	#(word, tf-idf for the token in the document).
	def tf_idf(self, tf, idf):
		
		#Initialize the table.
		tf_idf_table = {}
		
		#For each item in the term frequency table.
		for doc, value in tf.items():

			#Initialize the tf-idf vector.
			tf_idf_vector = []			
			
			#For each tuple in the tuple list.
			for item in value:
			
				token = item[0]		#Gets the word.
				tf = item[1]		#Gets the term frequency value for that word.
				
				#Compute the tf-idf value for the word.
				tf_idf = tf * idf[token]

				#Append the tf-idf value in the vector.
				tf_idf_vector.append( (token, tf_idf) )
			
			#Append the vector of tf-idf in the table.
			tf_idf_table[doc] = tf_idf_vector
		
		#Returns the table.
		return tf_idf_table

	#Sorts the vocabulary words regarding the tf-idf of each word in each document.
	def bestKeywords(self, data, idf):		
		
		#Initiallize the dictionary.
		total_tf_idf = {}
		
		#For each vocabulary word.
		for v in self.vocabulary:
		
			#Returns the row from the csv of the current word.
			row = data.loc[data["Words"] == v]
			
			#Sum all the tf-idf of the word for each document and substract the idf as it is also
			#summed due to the row in the csv file.	
			value = row.sum(axis=1).values[0] - idf[v]
			
			#Appends in the dictionary the word and its value.
			total_tf_idf[v] = value
		
		#Opens the file that will store the words.
		f = open(OUT_DIR + "best_keywords.txt","w+")
		
		#The words are sorted in descending order of the value and then stored in the file.
		for k, v in sorted(total_tf_idf.items(), key= lambda kv: kv[1], reverse=True):
			f.write(k + " -> " + str(v) + "\n")
			
		#Close the  file.
		f.close()
		
	#Sorts the documents regarding the tf-idf of each word belonging to each document.
	def bestSentences(self, data, documents):
	
		#Initialize the dicitonary.
		total_tf_idf = {}

		#For each document.
		for doc in documents:
			
			#Sums all the tf-idf values of the terms of the document.
			value = data[doc].sum()
			
			#Appends it in the dictionary.
			total_tf_idf[doc] = value				
		
		#Opens the file that will store the documents.
		f = open(OUT_DIR + "best_sentences.txt","w+")
		
		#The documents are sorted in descending order of the value and then stored in the file.
		for k, v in sorted(total_tf_idf.items(), key= lambda kv: kv[1], reverse=True):
			f.write(k + " -> " + str(v) + "\n")
			
		#Close the file
		f.close()
                
"""
	References:
                
	Term frequency:	https://stackoverflow.com/a/8272462
	Sort dictionary by values:	https://stackoverflow.com/a/613218
	
"""
