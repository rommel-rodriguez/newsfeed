import json
import urllib
import urllib.request as urllib2 
import re
from urllib.parse import urlencode
api_key = "" 
with open("newsfeed_keys.json", "r") as keys:
    api_key = json.load(keys)["cnn"]

print("CNN's Key Would be: {key}".format(key = api_key))
get_data = {
            "source":"cnn", 
            "sortBy":"top",
            "apiKey": api_key
           }

cnn_json_test = r'https://newsapi.org/v1/articles?' + urlencode(get_data)
headers = {}
user_agent = "Mozilla/5.0 (X11; Linux x86_64; rv:19.0) Gecko/20100101 Firefox/19.0"
headers["User-Agent"] = user_agent
def get_cnn_feed():
    opener = urllib2.build_opener()
    print("Trying to Open: {url}".format(url=cnn_json_test))
    request = urllib2.Request(cnn_json_test, headers = headers)
    response = opener.open(request)
    # Next We Print The Response Header, because it contains the character set
    # We Need to decode the json byte stream
    print("JSON Request Response Headers:")
    print(response.info())
    return response.read()

def get_nyt_dict():
    return json.loads(get_cnn_feed().decode("utf-8"))

if __name__ == '__main__':
    feed_bytes = get_cnn_feed()
    feed_utf8 = feed_bytes.decode("utf-8")
    feed_dict = json.loads(feed_utf8)

    #feed_dict = json.loads(feed_bytes, encoding="UTF-8") # Does not work for now

    print(feed_dict)
    assert False, "Test Break"
    with open("nyt_test.json", "w") as jf:
        jf.write(feed_utf8)
        jf.close()
