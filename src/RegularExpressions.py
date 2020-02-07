#CE314/887 - Natural Language Engineering.

#Victor Perez - vp19885  / 1900232
#Joel Valiente - jv19228 / 1900289

#Libraries needed for this program.
import nltk
import re
from src.assignment1.UrlDownloader import URLDownloader

class RegularExpressions():

    def __init__(self,url):
        """
        Downloads the given URL and declares the regex ready to be used.
        """
        self.downloader = URLDownloader()
        self.url = self.downloader.getPlainHtml(url)
        self.regex = re.compile('(\+\d{1,3} \d{2} \d{8}|\d{4,5} \d{6}|\d{11}|\+\d{1,3} \d{10}|\d{4} \d{10})' )

    def find(self):
        """
        Returns all the phone matches contained in the given URL.
        """
        matches = []
        for match in self.regex.findall(self.url):
            matches.append(match)
        
        matches = set(matches)
        self.print_output(matches)

    def print_output(self,result):
        """
        Prints the output of the find method execution in a friendly way
        """
        result = list(result)
        n = len(result)
        if n == 0:
            print("We did not found any match! :( ")
        elif n == 1:
            print("We found " + str(n) + " match! ")
        else:
            print("We found " + str(n) + " matches! ")

        for res in result:
            print("Telephone : " + str(res))



# findall regex : https://www.guru99.com/python-regular-expressions-complete-tutorial.html
# regex documentation : https://docs.python.org/3/howto/regex.html
# regex examles : https://www.w3schools.com/python/python_regex.asp
# reges phone validation : https://stackoverflow.com/questions/8634139/phone-validation-regex

