#Victor Perez - vp19885  / 1900232
#Joel Valiente - jv19228 / 1900289

import nltk
from nltk import re
from nltk import word_tokenize
from nltk.stem import WordNetLemmatizer

#Class for computing the Part-of-Speech tags given some tokens.
class POS():

	#Constructor.
    def __init__(self,args):
        self.args = args

    def tagPosTokens(self, tokens):
        """
        Computes the POS Tags for every token in the tokens list and stores this information in
        the /output folder.
        """
        if self.args.verbose: print("[INFO] Part Of Speach Tagging ...",end="\r",flush=True)
        
        #Compute the PoS tags for the given tokens.
        tags = nltk.pos_tag(tokens)
            
        #Store the result in a txt file.
        with open("output/" + "Pos.txt", 'w+') as f:
            for item in tags:
                f.write(str(item) + "\n")

        if self.args.verbose: print("\033[K[INFO] Part Of Speach Tagging ... Done")

        return tags
