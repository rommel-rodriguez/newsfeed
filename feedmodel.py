""" Simple Bundle of functions 
and Clases to Use in my News Project
"""

from __future__ import absolute_import 

__all__ = ['a', 'b', 'c']
__version__ = '0.1'
__author__ = 'Rodriguez Perez, Alberto'

import re

# The above is some example ordering from PEP8
class Article():
    def __init__(self,title="", description="", url="", image_url="", **kargs):
        ## Without the **kargs argument at the end, python will expect 
        ## every argument to have an equivalent in the 
        ## dict with the same name, in any other case it will produce an error 
        ## adding **kargs as argument will replace any argument value with 
        ## its equivalent in the dict passed to the function AND WILL NOT DO 
        ## ANYTHING with UNKWON arguments unless explicitly told so in the func-
        ## tion.
        self.title = title 
        self.description =  description
        self.url = url 
        self.image_url = image_url
        self.full_article = None
        self.image_bytes = None

    @classmethod    
    def load_article(cls, article):
        raise NotImplementedError

    def get_full_article(self):
        """ This method should retrive the full article from its publication
        Webpage and return it as a string.
        """
        raise NotImplementedError
    def __str__(self):
        info = "Title: {}\nDescription: {}\nURL: {}\nImage: {}\n".format(self.title
                                                                         ,self.description
                                                                         ,self.url
                                                                         ,self.image_url)
        return info

class CNNArticle(Article):
    def __init__(self, **kwargs):
        Article.__init__(self, **kwargs)
    @classmethod
    def load_article(cls, article):
        temp_url = article.get("urlToImage", "")
        del article["urlToImage"]
        article["image_url"] = temp_url
        return cls(**article)


class NYTArticle(Article):
    def __init__(self, **kwargs):
        Article.__init__(self, **kwargs)
        self.section = kwargs['section']
        ## Get extra data about the image, in case we need it.
        self.image_metadata = None
        try:
            self.image_metadata = kwargs['multimedia'][0]
        except BaseException as be:
            print("Some error Happened while trying to get NYT article's image" +
                    ' metadata.')
            print( be )
    @classmethod
    def load_article(cls, article):
        """ Loads a NYT article dictionary
            each NYT article dict has a multimedia
            array whose's elements are mostly 
            dictionaries with image metadata(size, url, etc ...)
            IMP : For now this function will only take ONE dict
                which's data will be used later  to display an image.
        """
        ## Get abtract and add it to dict as 'decription'.
        temp_summary = article.get("abstract", "")
        del article["abstract"]
        article["description"] = temp_summary

        ## Get metadata about ONE image
        #print("Debugging: \n {}".format(article))
        if article['multimedia']:
            temp_image = article['multimedia'][0]['url']
            article['image_url'] = temp_image

        return cls(**article)

if __name__ == '__main__':
    dummy_article = {
                    "title":"CNN Article Title",
                    "description":"CNN Description",
                    "url":"CNN's URL",
                    "urlToImage" : "CNN's url to image"
                    }
    cnn_art = CNNArticle.load_article(dummy_article)
    cnn_art2 = CNNArticle(description="XXX", title="YYY")
    print(cnn_art)
    print()
    print(cnn_art2)
    #margs = {"title": "Some Title", "description": "Some Description",
    #        "url": "Some URL", "image_url":"Some IMAGE URL", "unknowarg": "nothing"}
    #tar = Article(**margs)
    #art = Article()
    #print(tar)
    #print("Second Article: " + str(art))
    #print("#" * 20)
    #print(__doc__)
