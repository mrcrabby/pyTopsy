import urllib2, urllib
import os
import json

TOPSY_URL = "http://otter.topsy.com/"
TOPSY_AUTHORINFO = TOPSY_URL + "authorinfo.json"
TOPSY_EXPERTS = TOPSY_URL + "experts.json"
TOPSY_LINKPOST = TOPSY_URL + "linkposts.json"
TOPSY_LINKPOSTCOUNT = TOPSY_URL + "linkpostcount.json"
TOPSY_RELATED = TOPSY_URL + "related.json" 
TOPSY_SEARCH = TOPSY_URL + "search.json"
TOPSY_SEARCHCOUNT = TOPSY_URL + "searchcount.json"
TOPSY_SEARCHDATE = TOPSY_URL + "searchdate.json"
TOPSY_STATS = TOPSY_URL + "stats.json"
TOPSY_TRACEBACKS = TOPSY_URL + "trackbacks.json"
TOPSY_TRENDING = TOPSY_URL + "trending.json"
TOPSY_AUTHORSEARCH = TOPSY_URL + "authorsearch.json"

SEARCH = "search"
RELATED = "related"
AUTHORSEARCH = "authorsearch"
EXPERTS = "experts"

def decode_utf8(string):
    """ Returns the given string as a unicode string (if possible).
    """
    if isinstance(string, str):
        try: 
            return string.decode("utf-8")
        except:
            return string
    return unicode(string)
    
def encode_utf8(string):
    """ Returns the given string as a Python byte string (if possible).
    """
    if isinstance(string, unicode):
        try: 
            return string.encode("utf-8")
        except:
            return string
    return str(string)

u = decode_utf8
s = encode_utf8

# advanced dictionary
class TopsyDict(dict):
    def __init__(self):
        dict.__init__(self)
    def __getattr__(self, k):
        return self.get(k, u"")
    def __getitem__(self, k):
        return self.get(k, u"")
    def __setattr__(self, k, v):
        dict.__setitem__(self, u(k), v is not None and u(v) or u"")
    def __setitem__(self, k, v):
        dict.__setitem__(self, u(k), v is not None and u(v) or u"")

class URL():
    def __init__(self, url=TOPSY_SEARCH):
        self.url = url

    def download(self, params):
        """ Returns a list of results from Topsy that needs to be parsed
        """
        try:
            if isinstance(params, dict):
                q = urllib.urlencode(params)
            else:
                q = params
            dump = urllib2.Request(self.url + "?" + q)
            dump.add_header('User-Agent', 'Opera 666/Satan Edition')
            dump.add_header('Host', 'otter.topsy.com')
            opener = urllib2.build_opener()
            dump = opener.open(dump)
        except urllib2.URLError, msg:
            print msg
        feed = json.loads(dump.read())
        return feed

# main class
class Topsy():
    def __init__(self, type=EXPERTS):
        self.url = None
        self.type = type

    def _get_experts(self, params):
        feed = URL(url=TOPSY_EXPERTS).download(params)
        results = []
        for tweet in feed['response']['list']:
            r = TopsyDict()
            r.description = tweet.get("description")
            r.title = tweet.get("title")
            r.name = tweet.get("name")
            r.nick = tweet.get("nick")
            r.permalink = tweet.get("url")
            results.append(r)
        return results
    
    def _search_tweets(self, query="Django", author="", window="w"):
        if (author != ""):
            query = s(query) + "+from:" + author
        params = urllib.urlencode({"q": query,"window": window})
        feed = URL(url=TOPSY_SEARCH).download(params)
        results = []
        for tweet in feed['response']['list']:
            r = TopsyDict()
            r.permalin = tweet.get("trackback_permalink")
            r.description = tweet.get("content")
            r.title = tweet.get("title")
            r.nick = tweet.get("trackback_author_nick")
            results.append(r)
        return results
        
        
    def send_request(self, query, author="", window="w"):
        if (self.type == EXPERTS):
            return self._get_experts(query)
        elif (self.type == SEARCH):
            return self._search_tweets(query=query, window=window, author=author)
