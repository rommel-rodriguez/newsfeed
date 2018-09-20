import json
import re
import os
import urllib
import urllib.request as urllib2 
from feedmodel import CNNArticle
from feedmodel import NYTArticle
from urllib.parse import urlencode

headers = {}
user_agent = "Mozilla/5.0 (X11; Linux x86_64; rv:19.0) Gecko/20100101 Firefox/19.0"
headers["User-Agent"] = user_agent
opener = urllib2.build_opener()
all_articles = [] 
feeds_folder = 'feeds'
feed_files = os.listdir(feeds_folder)
def get_nyt_feed():
    """ Retrieves all interests as stated in the nyt.json file
        in json format and writes them to files.
        TODO: 
            -Make use of urlencode for the request 
            -Get our credentials from newsfeed_keys.json 
            -Consider moving interest an keys to a single file
                called feedconfig.json
    """
    nyt_json_url = ""
    nyt_topic = None
    with open("nyt.json","r") as json_file:
        nyt_info = json.load(json_file)
    for interest in  nyt_info["interest"]:
        nyt_topic_file = open("feeds/nyt_{}.json".format(interest), "wb") 
        nyt_json_url = nyt_info['base_url'] + interest + "." + nyt_info['extension'][0]\
                + "?api-key=" + nyt_info['APIKey']['top-stories']
        request = urllib2.Request(nyt_json_url, headers = headers)
        response = opener.open(request)
        #print("HTTP Header:")
        #print(response.info()) # Look for the encoding
        content = response.read() ###Content in raw bytes

        #if content:
        #    print("Got NYT %s Feed" % (interest, ))
        #    nyt_topic_file.write(content)

        nyt_topic_file.close()


def get_cnn_feed():
    """ Retrieves cnn's feed and writes it to a json file.
    """
    api_key = "" 
    cnn_feed_file = 'feeds/cnn_daily.json'
    with open("newsfeed_keys.json", "r") as keys:
        api_key = json.load(keys)["cnn"]

    #print("CNN's Key Would be: {key}".format(key = api_key))
    get_data = {
                "source":"cnn", 
                "sortBy":"top",
                "apiKey": api_key
            }
    cnn_json_test = r'https://newsapi.org/v1/articles?' + urlencode(get_data)
    headers = {}
    user_agent = "Mozilla/5.0 (X11; Linux x86_64; rv:19.0) Gecko/20100101 Firefox/19.0"
    headers["User-Agent"] = user_agent
    opener = urllib2.build_opener()
    request = urllib2.Request(cnn_json_test, headers = headers)
    response = opener.open(request)
    #print("JSON Request Response Headers:")
    #print(response.info())
    with open(cnn_feed_file, 'wb') as cnn_feed_file:
        cnn_feed_file.write(response.read())
        cnn_feed_file.close()

def are_feeds_updated():
    """ Checks if feed files need to be redownloaded
        returns: True if files are up to date, false if they need to 
            be refreshed.
    """
    return True

def extract_cnn_articles():
    cnn_articles = None
    with open(feeds_folder + '/cnn_daily.json', 'r') as cnn_feed_file:
        cnn_articles = json.load(cnn_feed_file)['articles']
        cnn_feed_file.close()
    
    for article in cnn_articles:
        all_articles.append(CNNArticle.load_article(article))

def extract_nyt_articles():
    nyt_articles = [] 
    nyt_pattern = re.compile(r'.*nyt_.*\.json$')
    for json_file in feed_files:
        json_file = "{}/{}".format(feeds_folder, json_file)
        #print("FILE: {} in feeds directory.".format(json_file))
        if nyt_pattern.match(json_file):
            #print("FILE: {} matched the pattern".format(json_file))
            with open(json_file, 'r') as nyt_feed_file:
                section_articles = json.load(nyt_feed_file)['results']
                nyt_articles += section_articles
                nyt_feed_file.close()
    
    for article in nyt_articles:
        all_articles.append(NYTArticle.load_article(article))

def run_feed_getters():
    """ Refreshes all the feed json files by running  the different
    methods for each feed.
    TODO: Automate this to find and use all get_xxx_feed functions, add
        add some mechanism so this is only ran when needed.
    """
    get_nyt_feed()
    get_cnn_feed()

def fill_feed_list():
    """ Fills the articles array by running all the feed json extractors.
    TODO: automate this the same way as with run_feed_getters and make this run
        all functions in this module that follow the parten extra_xxx_articles.
    returns: the feed array 'all_articles'.
    """
    extract_cnn_articles()
    extract_nyt_articles()
    return all_articles

if __name__ == '__main__':
    #get_nyt_feed()
    #get_cnn_feed()
    #extract_cnn_articles()
    extract_nyt_articles()
    for article in all_articles:
        print(article)
