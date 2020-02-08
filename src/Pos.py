import nltk
from nltk import re
from nltk import word_tokenize
from nltk.stem import WordNetLemmatizer

class POS():

    def __init__(self,args):
        self.args = args

    def tagPosTokens(self, tokens):
        """
        Computes the POS Tags for every token in the tokens list and stores this information in
        the /output folder.
        """
        if self.args.verbose: print("[INFO] Part Of Speach Tagging ...",end="\r",flush=True)
        tags = nltk.pos_tag(tokens)
            
        with open("output/" + "Pos.txt", 'w+') as f:
            for item in tags:
                f.write(str(item) + "\n")

        if self.args.verbose: print("\033[K[INFO] Part Of Speach Tagging ... Done")
        return tags