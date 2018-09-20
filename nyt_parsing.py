import json
import urllib
import urllib.request as urllib2 
import re

nyt_json_url = ""
nyt_topic = None
with open("nyt.json","r") as json_file:
    nyt_info = json.load(json_file)
headers = {}
user_agent = "Mozilla/5.0 (X11; Linux x86_64; rv:19.0) Gecko/20100101 Firefox/19.0"
headers["User-Agent"] = user_agent
opener = urllib2.build_opener()
for interest in  nyt_info["interest"]:
    topic_file = open("nyt_{}.json".format(interest), "wb") 
    nyt_json_url = nyt_info['base_url'] + interest + "." + nyt_info['extension'][0]\
            + "?api-key=" + nyt_info['APIKey']['top-stories']
    ##print(nyt_json_url)
    ##assert False, "URL Test"
    request = urllib2.Request(nyt_json_url, headers = headers)
    response = opener.open(request)
    print("HTTP Header:")
    print(response.info()) # Look for the encoding
    content = response.read() ###Content in raw bytes
    print('='*20 + ">" + "CONTENT")
    #print(content.decode())
    #topic_file.write(bytes(content.decode(), "utf-8"))
    topic_file.write(content)
    topic_file.close()
    # Test if conte.decode
    #assert False, "Test Break Point"
    break
with open("nyt_world.json", "r") as feed_file:
    nyt_topic = json.load(feed_file)
    print("SUCCESS LOADING JSON FILE")
    feed_file.close()

for key in nyt_topic:
    if key == "results":
            article_array = nyt_topic[key]
            for rkey, value in article_array[0].items():
                print("Key ==> {}: {}".format(rkey, value))




