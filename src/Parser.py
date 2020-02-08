from src.UrlDownloader import URLDownloader
from bs4 import BeautifulSoup
from bs4.element import Comment
from definitions import OUT_DIR

"""
This class will Parse a given URL and return all the visible text in it. 
"""
class Parser():

    def __init__(self,args):
        self.URLDownloader = URLDownloader(args)
        self.args = args

    """
    Parses the given url and extracts all the visible information. 
    * Arguments : The url to parse
    * Returns : A string with all the text parsed.
    """ 
    def parse(self):
        if self.args.verbose: print("[INFO] Parsing HTML ...",end="\r",flush=True)
        html = self.URLDownloader.getPlainHtml(self.args.url)
        soup = BeautifulSoup(html, 'html.parser')
        texts = soup.findAll(text=True)
        visible_texts = filter(self.tag_visible, texts)  
        if self.args.verbose: print("\033[K[INFO] Parsing HTML ... Done")
        text = "\n".join(t.strip() for t in visible_texts)
        with open(OUT_DIR + "html_parsing.txt", 'w+') as f:
            f.write(text)
        
        f.close()
        return text

    """
    Checks if a tag is considered visible or not
    * Arguments : An html element
    * Returns : True if the tag is visible, false otherwise
    """
    def tag_visible(self,element):
        if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
            return False
        if isinstance(element, Comment):
            return False
        return True
