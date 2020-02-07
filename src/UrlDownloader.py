#CE314/887 - Natural Language Engineering.

#Victor Perez - vp19885  / 1900232
#Joel Valiente - jv19228 / 1900289

#Libraries needed for this program.
import urllib.request

#Download the content between <p> and </p> html tags given a url.
class URLDownloader():
	
	def getPlainHtml(self, url):
		try:
			response = urllib.request.urlopen(url)		#Open the given url. [1]
			weirdHtml = response.read()					#Extracts html in bytes. [1]
			plainHtml = weirdHtml.decode("utf-8")		#Decode it to utf-8 format.
			
		except Exception as e: 	#In the case of some error raise it. [2]
			raise e
			
		return plainHtml	#Return the html.
			
"""	References:
	-> [1] Urllib management: https://docs.python.org/2/howto/urllib2.html	
	-> [2] Exceptions in python : https://stackoverflow.com/questions/1483429/how-to-print-an-exception-in-python
"""
