#CE314/887 - Natural Language Engineering.

#Victor Perez - vp19885  / 1900232
#Joel Valiente - jv19228 / 1900289

#Libraries needed for this program.
import nltk
from nltk import re
from nltk import word_tokenize
from nltk.util import ngrams
from nltk import FreqDist
from collections import Counter
from definitions import DATA_DIR

def tokenizeDataFromAFile(txtFile):
	"""
	Reads the given file and returns a list containing its lines
	"""
	if not re.search(".txt", txtFile):
		txtFile += ".txt"
		
	return open(DATA_DIR + txtFile, "r").read().splitlines()	#[1] [2]
	
class Ngram():
	"""
	This class has methods to carry out the unigram and bigram exercises
	"""

	def __init__(self, n):

		self.train = tokenizeDataFromAFile("sampledata.txt")		#Train data from data folder.
		self.voc = tokenizeDataFromAFile("sampledata.vocab.txt")	#Vocabulary of the n-gram.
		#Parameter n of n-grams (=1 for unigram and =2 for bigram).
		self.n = n
		
		self.setVocabulary()				
		self.train = self.cleanTrain()		
		
		self.N = len( ' '.join(self.train).split() )
		
	def setVocabulary(self):
		"""
		Adds missing words in the vocabulary.
		"""
		self.voc.append("UNK")			#Unknown words.
		
		if(self.n != 1):				#In the case of bigram language models:
			self.voc.append("<s>")		
			self.voc.append("</s>")		
		
	def cleanTrain(self):
		"""
		Cleans '<s>' and '</s>' tokens in unigram language models.
		"""
		if(self.n == 1):	#For unigram language models:
			newTrain = []
			
			for s in self.train:
			
				sentence = s.split(" ")
				newSentence = ""
				
				for word in sentence:
				
					if( word != "<s>" and word != "</s>" ): #Clean '<s>' and '</s>'
						newSentence += word + " "
				
				newTrain.append( newSentence[:-1] )
				
			return newTrain
		
		else:					#For bigrams, do not clean them as they are part of the vocabulary.
			return self.train
			
	def countOneWord(self, word):
		"""
		Compute the number of repetitions for the given word in the vocabulary
		In the word is not contained in the vocabulary, it returns the number of unknown words
		"""
		count = 0
		
		for s in self.train:
		
			sentence = s.split(" ")
			fdist = FreqDist(sentence)		#Computes the frequency distribution of the sentence.
			
			try:
				if(word in self.voc):			#If the word is in the vocabulary:
					count += fdist.get(word)	#Compute the number of repetitions using the frequency distribution.
					
				else:			
					
					if(word != '<s>' and word != '</s>'):	#If is an unknown word:
					
						for key in fdist.keys():			
							
							if( key not in self.voc ):		
								count += fdist.get(key)		#Compute the repetitions for all unknown words of each sentence.
			except:
				pass
				
		return count
		
	def countTwoWords(self):
		"""
		Counts the times two words are found together in the training data. Also known as a bigram
		"""
		counts = {}
		
		for s in self.train:
		
			sentence = s.split(" ")
		
			ngram = ngrams(sentence, self.n)		#Creates the bigram of each sentence. [3]
			counter = Counter(ngram)				#Computes the number of repetitions of each pair of words.
			
			#Counter is a dictionary containing as key (word1, word2) and as value the number of repetitions of that pair of words.
			for element in counter:					
			
				localProb = ""
				
				for word in element[:]:				#For each word of the key:
					
					if( word in self.voc ):			#If the word is in the vocabulary, appends it with a space at the end of the word.	
						localProb += word + " "
						
					else:							#Appends unknown word token and a space after that.
						localProb += "UNK "						
		
				localProb = localProb[:-1]		#Cleans the last space in order to format the string as "word1 word2".
				
				#Store the generated key "word1 word2" and its repetitions in a new dictionary.
				try:
					counts[localProb] += counter.get(element)	#If the key exist, add the repetitions to the current value.
					
				except:
					counts[localProb] = counter.get(element)	#Else, creates a new element in the dictionary.
		
		self.counts = counts	#Class atribute to be used later on.
		return counts			#Returns the resulting dictionary.
		
	def printResultsTable(self, data, token_list):
		"""
		Prints a table with the given data and the given columns/rows.
		"""
		str_l = 5	#As we are rounding the decimals to 3, the maximun lenght of each probability is 5: "0", ".", and the three decimals.
		
		print(" ".join(['{:>{length}s}'.format(t, length = str_l) for t in [" "] + token_list]))

		for t, row in zip(token_list, data):
		    print(" ".join(['{:>{length}s}'.format(str(x), length = str_l) for x in [t] + row]))
		
	def computeProbabilities(self):
		"""
		Compute the probabilities of the training data depending of which n-gram we have.
		"""
		if(self.n == 1):
			return self.computeProbabilitiesUnigram()
			
		elif(self.n == 2):
			return self.computeProbabilitiesBigram()
			
		else:
			return "Error: this class only supports unigram and bigram language models."
	
	def computeProbabilitiesUnigram(self):
		"""
		#Compute the probabilities for the unigram model.
		"""
		print("=== UNIGRAM MODEL ===")
		print("- Unsmoothed -")
		self.unsmoothedProbs = {}			#Resulting unsmoothed probabilties.
		
		for word in self.voc:
		
			prob = self.countOneWord(word)/self.N		#Compute the unsmoothed probability for each word of the vocabulary.
			prob = round(prob, 3)						#Round the probability to three decimals. [5]
			self.unsmoothedProbs[word] = prob			#Store it in the unsmoothed probabilities dictionary.
			
			#Prints this information though the system output (terminal). [4]
			print(word + ": ", end="")
			print(prob, end="")
			print("  ", end="")
			
		print("\n\n- Smoothed -")
		self.smoothedProbs = {}				#Resulting smoothed probabilties.
		
		for word in self.voc:
		
			#Compute the smoothed probability for each word of the vocabulary.
			prob = ( self.countOneWord(word) + 1 )/( self.N + len(self.voc) )
			prob = round(prob, 3)						#Round the probability to three decimals. [5]
			self.smoothedProbs[word] = prob				#Store it in the smoothed probabilties dictionary.
			
			#Prints this information though the system output (terminal). [4]
			print(word + ": ", end="")
			print(prob, end="")
			print("  ", end="")
		
		print("\n")

	def computeProbabilitiesBigram(self):
		"""
		Computes de probability for the bigram model.
		"""
		print("=== BIGRAM MODEL ===")
		print("- Unsmoothed -")
		self.unsmoothedProbs = {}		#Resulting unsmoothed probabilties.
		
		self.countTwoWords()			#Computes the repetitions of each pair of words from the training data.
		
		data = []						#List to be used for printing the table.

		for wordA in self.voc:						#For each word in the vocabulary (rows):
		
			probs = []								#List of probabilties (for printing the table).
			
			for wordB in self.voc:					#For each word in the vocabulary (columns):
				
				dictKey = wordA + " " + wordB		#Defines the key of the two words that counts dictionary contains.
				
				if(self.countOneWord(wordA) != 0):
					
					#wordA -> in row, wordB-> in column: P(wordB|wordA) = count(wordA,wordB)/count(wordA)
					prob = self.counts.get(dictKey, 0)/self.countOneWord(wordA)		#Compute the unsmoothed probability for each pair of words of the vocabulary.
					prob = round(prob, 3)			#Round the probability to three decimals. [5]

				else:
					prob = 0.000
				
				probs.append(prob)						#Appends the probability to the probs.
				self.unsmoothedProbs[dictKey] = prob	#Store the probability in the unsmoothed probabilties dictionary.
			
			data.append(probs)				#Appends all the probabilities list for of wordA for all the columns in the data list.
			
		self.printResultsTable(data, self.voc)		#Prints the table.
		
		print("\n- Smoothed -")
		self.smoothedProbs = {}			#Resulting smoothed probabilties.
		
		data = []						#List to be used for printing the table.

		for wordA in self.voc:						#For each word in the vocabulary (rows):
		
			probs = []								#List of probabilties (for printing the table).
			
			for wordB in self.voc:					#For each word in the vocabulary (columns):
				
				dictKey = wordA + " " + wordB		#Defines the key of the two words that counts dictionary contains.
				
				if(self.countOneWord(wordA) != 0):
				
					#wordA -> in row, wordB-> in column: P(wordB|wordA) = count(wordA,wordB) + 1/count(wordA) + |vocabulary|
					prob = self.counts.get(dictKey, 0) + 1
					prob = prob/( self.countOneWord(wordA) + len(self.voc) )	#Compute the smoothed probability for each pair of words of the vocabulary.
					prob = round(prob, 3)			#Round the probability to three decimals. [5]

				else:
					prob = 0.000

				probs.append(prob)						#Appends the probability to the probs.
				self.smoothedProbs[dictKey] = prob		#Store the probability in the smoothed probabilties dictionary.
			
			data.append(probs)				#Appends all the probabilities list for of wordA for all the columns in the data list.
			
		self.printResultsTable(data, self.voc)		#Prints the table.
		print()
		
class Testing():
	"""
	This class will test a given data against the computed probabilities by the above Ngram() class.
	It will output the overall probability for a given sentence
	"""		
	def testing(self):

		testData = tokenizeDataFromAFile("sampledata.txt")		#Testing data from the data folder.
		
		unigram = Ngram(1)										#Creates an unigram language model.
		unigram.computeProbabilities()							#Computes the probabilities of the training data.
		unigramSmoothedProbs = unigram.smoothedProbs			#Gets the smoothed probabilities of the unigram.
		
		bigram = Ngram(2)										#Creates a bigram language model.
		bigram.computeProbabilities()							#Computes the probabilities of the training data.
		bigramSmoothedProbs = bigram.smoothedProbs				#Gets the smoothed probabilities of the bigram.
		
		unigramProb = 1			#Initial unigram and bigram probabilties.
		bigramProb = 1
		
		data = {}				#Dictionary that will store the testing information.
		
		print("\n== SENTENCE PROBABILITIES ==")
		print("sent\t\t\tuprob\t\tbiprop")
		
		for s in testData:						#For each sentence of the testing data:
		
			sentence = s.split(" ")
			
			#Unigram sentence probability.
			for word in sentence:				#For each word of the sentence.
				
				if( word in unigram.voc ):		#Compute the probability of the word if it belongs to the vocabulary.
					unigramProb = unigramProb * unigramSmoothedProbs.get(word)
					
				else:
					if(word != '<s>' and word != '</s>'):	#If the word is an unknown word:
						unigramProb = unigramProb * unigramSmoothedProbs.get("UNK")
				
			ngram = ngrams(sentence, 2)		#Bigram for each sentence of testing data. [3]
			counter = Counter(ngram)		#Computes the repetitions of each word pair.
			
			#Bigram sentence probability.
			for element in counter:				#For each word of the sentence.
			
				dictKey = element[0] + " " + element[1]		#Creates the key given the two words and then compute its probability.
				bigramProb = bigramProb * bigramSmoothedProbs.get(dictKey)
			
			#Prints the results through system output (terminal). [4] [7]
			print(' '.join(sentence), end="")
			print('\t', end="")		
			print('%.3g' % unigramProb, end="")
			print('\t', end="")		
			print('%.3g' % bigramProb)
			
			data[' '.join(sentence)] = (unigramProb, bigramProb)	#Store the sentence, unigram probability and bigram probability in a dictionary.
			
		return data	
			
"""	References:
	
	-> [1] Read a file: https://www.w3schools.com/python/python_file_open.asp
	-> [2] Split lines from a file: https://stackoverflow.com/a/275659
	-> [3] N-grams nltk: https://stackoverflow.com/a/32442106
	-> [4] Print without new line: https://www.stechies.com/python-print-without-newline/
	-> [5] Round a float number: https://stackoverflow.com/a/13479195
	-> [6] Print table format: https://stackoverflow.com/a/51595466
	-> [7] Rounding exponentials numbers; https://stackoverflow.com/questions/19077467/decimal-digits-in-python-with-e
"""