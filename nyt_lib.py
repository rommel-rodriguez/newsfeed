import json
import urllib
import urllib.request as urllib2 
import re

def getAMap():
    nyt_json_url = ""
    with open("nyt.json","r") as json_file:
        nyt_info = json.load(json_file)
    headers = {}
    user_agent = "Mozilla/5.0 (X11; Linux x86_64; rv:19.0) Gecko/20100101 Firefox/19.0"
    headers["User-Agent"] = user_agent
    opener = urllib2.build_opener()
    for interest in  nyt_info["interest"]:
        nyt_json_url = nyt_info['base_url'] + interest + "." + nyt_info['extension'][0]\
                + "?api-key=" + nyt_info['APIKey']['top-stories']
        ##print(nyt_json_url)
        ##assert False, "URL Test"
        request = urllib2.Request(nyt_json_url, headers = headers)
        response = opener.open(request)
        content = response.read() ###Content in raw bytes
        decoded_content = content.decode("iso-8859-1") ## Easy way no need to use regexp

        nyt_section_map = json.loads(decoded_content)
        return nyt_section_map

def getHttp(url):
    headers = {}
    user_agent = "Mozilla/5.0 (X11; Linux x86_64; rv:19.0) Gecko/20100101 Firefox/19.0"
    headers["User-Agent"] = user_agent
    opener = urllib2.build_opener()
    request = urllib2.Request(url, headers = headers)
    response = opener.open(request)
    content = response.read() ###Content in raw bytes
    return content

