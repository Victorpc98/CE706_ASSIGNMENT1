#Victor Perez - vp19885  / 1900232
#Joel Valiente - jv19228 / 1900289

import urllib.request
import sys

#Download the content between <p> and </p> html tags given a url.
class URLDownloader():

	#Constructor.
	def __init__(self,args):
		self.args = args
	
	#Returns the visible text given the url.
	def getPlainHtml(self, args):

		try:

			if self.args.verbose: print("[INFO] Downloading URL ...",end="\r",flush=True)

			response = urllib.request.urlopen(self.args.url)		#Open the given url. [1]
			weirdHtml = response.read()					#Extracts html in bytes. [1]
			plainHtml = weirdHtml.decode("utf-8")		#Decode it to utf-8 format.
			
		except urllib.error.URLError: 	#In the case of some error raise it. [2]

			print("[ERROR] {0} can't be reached. Finishing execution.".format(self.args.url))
			sys.exit()
			
		if self.args.verbose: print("\033[K[INFO] Downloading URL ... Done")

		return plainHtml	#Return the html.
			
"""	References:
	-> [1] Urllib management: https://docs.python.org/2/howto/urllib2.html	
	-> [2] Exceptions in python : https://stackoverflow.com/questions/1483429/how-to-print-an-exception-in-python
"""
