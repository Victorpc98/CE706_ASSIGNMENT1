from nltk import FreqDist
from nltk.corpus import stopwords
from definitions import OUT_DIR
import math
import pandas as pd
class KeywordsFilter():

    def __init__(self,args):
        self.args = args

    def filter(self,tokens,documents):
        if self.args.verbose: print("[INFO] Selecting Keywords ...",end="\r",flush=True)
        tokens = self.remove_stopwords(tokens) # Remove stopwords
        tf = self.termFrequency(tokens) # Frequency for each token
        tokens = set(tokens) # Convert to set so duplicates tokens are delated
        res = []
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

    # Returns a dictionary. Get frequency of an element using freqdist[token]
    def termFrequency(self, tokens):
        fdist = FreqDist(tokens)
        return dict(fdist)

    # Computes the IDF as [log(N/dft)]. Where N is the # of documents 
    # in the collection and dft is the Document Term Frequency
    def inverseDocFrequency(self, dft, token, documents):
        idf = math.log(len(documents)/dft)
        return idf

    # (DFT) Returns the number of documents where the term appears at
    def documentFrequencyTerm(self,term,documents):
        count = 0
        for doc in documents:
            if(term in doc):
                count += 1
                
        return count

    # Computes tf.idf 
    def tfIdf(self, tf, idf):
        return tf * idf

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
                
            