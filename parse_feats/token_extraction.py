# -*- coding: utf-8 -*-
'''
Created on 28 Nov 2013

@author: michal

Functions allowing loading various tokens from an XML file with annotations. 

data in argument lists = (filename, preloaded file using xml_tokens)
'''
import xml.etree.ElementTree as ET
from utils.fileop import convert_url2fname
import nltk
from nltk.corpus import stopwords
stop = stopwords.words('english')
stop.remove('not')
stop.remove('no')
STOPWORDS_SET = set(stop)

HASHTAG_SYMBOL = "#"
URL_SYMBOL = "URL"
AT_SYMBOL = "@"
RT_SYMBOL = 'RT'
USER_SYMBOL = 'USR'
TOKEN_XMLTAG = 'Token'
KIND_ATTRIBUTE = 'kind'
STRING_ATTRIBUTE = 'string'
CATEGORY_ATTRIBUTE = 'category'
PUNCTUATION_SYMBOL = "punctuation"
HASHTAG_PREFIX = "TAG"

#For testing purposes only:
from utils.testing import A

def author(data):
    '''
    Extracts author from a filename..
    '''
    return data["author"]

def xml_tokens(inputxml_fname, from_file=True):
    '''
    Load root of the xml which is the uppest node which has Token nodes inside.
    '''
    if from_file:
        tree = ET.parse(inputxml_fname)
        root = tree.getroot()
    else:
        root = ET.fromstring(inputxml_fname)
    children = []
    #get rid of nesting tags, such as Tweet, of which there 
    #can be a multiple number
    while root.find(TOKEN_XMLTAG)==None:
        root = root[0]
    for child in root:
        if child.tag==TOKEN_XMLTAG:
            children.append(child)
    return children

def hashtag(data):
    '''
    Extracts hashtags from XML file, embedded in Token tags.
    '''
    return hashtag_raw(data["tokens"])

def hashtag_raw(children):
    '''
    >>> hashtag_raw([A({KIND_ATTRIBUTE: PUNCTUATION_SYMBOL, STRING_ATTRIBUTE: ","}), \
    A({KIND_ATTRIBUTE: PUNCTUATION_SYMBOL, STRING_ATTRIBUTE: HASHTAG_SYMBOL}), \
    A({KIND_ATTRIBUTE: URL_SYMBOL, STRING_ATTRIBUTE: "www.blebu.pl"}), \
    A({KIND_ATTRIBUTE: PUNCTUATION_SYMBOL, STRING_ATTRIBUTE: HASHTAG_SYMBOL}), \
    A({KIND_ATTRIBUTE: STRING_ATTRIBUTE, STRING_ATTRIBUTE: "MaryJane"})])
    ['#MaryJane']
    '''
    res = []
    prev_hash = False
    for child in children:
        if child.attrib[KIND_ATTRIBUTE] != PUNCTUATION_SYMBOL and \
        child.attrib[KIND_ATTRIBUTE] != URL_SYMBOL:
            if prev_hash:
                res.append( HASHTAG_SYMBOL+child.attrib[STRING_ATTRIBUTE] )
        #update info if it is a hashtag: 
        prev_hash = (child.attrib[KIND_ATTRIBUTE] == PUNCTUATION_SYMBOL and \
                     child.attrib[STRING_ATTRIBUTE] == HASHTAG_SYMBOL)
    return res

def retweeted(data):
    '''
    Extracts login of the original tweet author. If there is none, just don't
    return anything.
    
    It is found in the following way: if we have 2 consecutive tokens: RT and 
    a word of category USR, than the tweet was retweeted from that word
    of category USR.
    '''
    return retweeted_raw(data["tokens"])

def retweeted_raw(children):
    '''
    >>> retweeted_raw([A({KIND_ATTRIBUTE: PUNCTUATION_SYMBOL, STRING_ATTRIBUTE: ",", CATEGORY_ATTRIBUTE:"BLA1"}), \
    A({KIND_ATTRIBUTE: PUNCTUATION_SYMBOL, STRING_ATTRIBUTE: HASHTAG_SYMBOL, CATEGORY_ATTRIBUTE:"BLA2"}), \
    A({KIND_ATTRIBUTE: URL_SYMBOL, STRING_ATTRIBUTE: "www.blebu.pl", CATEGORY_ATTRIBUTE:"BLA3"}), \
    A({KIND_ATTRIBUTE: PUNCTUATION_SYMBOL, STRING_ATTRIBUTE: RT_SYMBOL, CATEGORY_ATTRIBUTE:"BLA4"}), \
    A({KIND_ATTRIBUTE: STRING_ATTRIBUTE, STRING_ATTRIBUTE: "@MaryJane", CATEGORY_ATTRIBUTE:"BLA5"})])
    ['MaryJane']
    '''
    res = []
    prev_rt = False
    for child in children:
        if prev_rt or child.attrib[CATEGORY_ATTRIBUTE] == USER_SYMBOL:
            if child.attrib[STRING_ATTRIBUTE].startswith("@"):
                res.append( child.attrib[STRING_ATTRIBUTE][1:] )
            else:
                res.append( child.attrib[STRING_ATTRIBUTE] )
        #update info about RT
        prev_rt = child.attrib[STRING_ATTRIBUTE] == RT_SYMBOL
    return res

def allnetwork(data):
    '''
    Combination of author and retweeted.
    '''
    return [author(data)] + retweeted(data)

def url_addresses(inputxml_fname):
    '''
    Extracts urls from XML file, embedded in Token tags.
    '''
    return [child.attrib[STRING_ATTRIBUTE] for child in xml_tokens(inputxml_fname) 
            if child.attrib[KIND_ATTRIBUTE] == URL_SYMBOL]
urlcnt = 0
def url_content(data, PATH2URLS):
    '''
    Extracts urls from XML file, embedded in Token tags.
    
    Reading of appropriate URLs happens only once and is stored within the data.
    '''
    if "url" in data:
        return data["url"]
    
    res = []
    for child in data["tokens"]: 
        if child.attrib[KIND_ATTRIBUTE] == URL_SYMBOL:
            try:
                with open(PATH2URLS + \
                            convert_url2fname(child.attrib[STRING_ATTRIBUTE]), 'r') as f:
                    for l in f:
                        res += l.split()

                #print "success:", PATH2URLS + \
                #convert_url2fname(child.attrib[STRING_ATTRIBUTE])
            except:
                pass
    global urlcnt
    if res != []:
        urlcnt += 1
        #print "[url_content] detected non-empty", urlcnt
    data["url"] = res
    return res

def words(data):
    '''
    Extracts tokens from XML file, embedded in Token tags, ignores punctuation 
    and URL. Also, if previous tag was a '#', then we do not yield the string 
    (as it is most likely a hashtag).
    '''
    return words_raw(data["tokens"], lower=False)


def words_lower_stemmed(data):
    from nltk.stem.porter import PorterStemmer
    #Create a new Porter stemmer.
    stemmer = PorterStemmer()
    
    return [stemmer.stem(w) for w in words_lower(data)]

def words_lower(data):
    res = []
    for w in words_raw(data["tokens"], lower=True):
        wl = w.split() 
        wl = reduce(lambda a, b: a+b, map(lambda x: x.split("-"), wl))
        wl = reduce(lambda a, b: a+b, map(lambda x: x.split("_"), wl))
        res += wl
    filter(lambda x: x not in STOPWORDS_SET, res)
    return res

def poss(data, filter_fun=None):
    '''
    Extracts POS tags from XML file.
    '''
    return poss_children(data["tokens"], filter_fun)

def poss_children(children, filter_fun=None):
    '''
    >>> poss_raw([A({KIND_ATTRIBUTE: PUNCTUATION_SYMBOL, STRING_ATTRIBUTE: ",", CATEGORY_ATTRIBUTE:"BLA1"}), \
    A({KIND_ATTRIBUTE: PUNCTUATION_SYMBOL, STRING_ATTRIBUTE: HASHTAG_SYMBOL, CATEGORY_ATTRIBUTE:"BLA2"}), \
    A({KIND_ATTRIBUTE: URL_SYMBOL, STRING_ATTRIBUTE: "www.blebu.pl", CATEGORY_ATTRIBUTE:"BLA3"}), \
    A({KIND_ATTRIBUTE: PUNCTUATION_SYMBOL, STRING_ATTRIBUTE: HASHTAG_SYMBOL, CATEGORY_ATTRIBUTE:"BLA4"}), \
    A({KIND_ATTRIBUTE: STRING_ATTRIBUTE, STRING_ATTRIBUTE: "MaryJane", CATEGORY_ATTRIBUTE:"BLA5"})])
    ['BLA1', 'BLA2', 'TAGBLA3', 'BLA4', 'TAGBLA5']
    '''
    res = []
    prev_hash = False
    for child in children:
        if filter_fun and filter_fun(child):
            continue
        if child.attrib[STRING_ATTRIBUTE] == HASHTAG_SYMBOL:
            prev_hash = True
        else:
            res.append(int(prev_hash)*HASHTAG_PREFIX+child.attrib[CATEGORY_ATTRIBUTE])
            prev_hash = False
            
    return res

def strings_raw(data, filter_fun=None):
    print "[strings_raw] data:", data
    return strings_children(data["tokens"], filter_fun)

def strings_children(children, filter_fun=None):
    '''
    Printing strings as they are in the xmls, only fixing the hashtags.
    
    >>> words_raw([A({KIND_ATTRIBUTE: PUNCTUATION_SYMBOL, STRING_ATTRIBUTE: ",", CATEGORY_ATTRIBUTE:"BLA1"}), \
    A({KIND_ATTRIBUTE: PUNCTUATION_SYMBOL, STRING_ATTRIBUTE: HASHTAG_SYMBOL, CATEGORY_ATTRIBUTE:"BLA2"}), \
    A({KIND_ATTRIBUTE: URL_SYMBOL, STRING_ATTRIBUTE: "www.blebu.pl", CATEGORY_ATTRIBUTE:"BLA3"}), \
    A({KIND_ATTRIBUTE: PUNCTUATION_SYMBOL, STRING_ATTRIBUTE: RT_SYMBOL, CATEGORY_ATTRIBUTE:"BLA4"}), \
    A({KIND_ATTRIBUTE: STRING_ATTRIBUTE, STRING_ATTRIBUTE: "@MaryJane", CATEGORY_ATTRIBUTE:"BLA5"})])
    [',', 'RT', '@MaryJane']
    '''
    res = []
    prev_hash = False
    for child in children:
        if filter_fun and filter_fun(child):
            continue
        if child.attrib[STRING_ATTRIBUTE] == HASHTAG_SYMBOL:
            prev_hash = True
        else:
            if child.attrib[KIND_ATTRIBUTE] != URL_SYMBOL:
                res.append(int(prev_hash)*HASHTAG_SYMBOL+child.text)
            else:
                res.append("URL_ADDRESS")
            prev_hash = False
    return res

def words_raw(children, lower=False):
    '''
    >>> words_raw([A({KIND_ATTRIBUTE: PUNCTUATION_SYMBOL, STRING_ATTRIBUTE: ",", CATEGORY_ATTRIBUTE:"BLA1"}), \
    A({KIND_ATTRIBUTE: PUNCTUATION_SYMBOL, STRING_ATTRIBUTE: HASHTAG_SYMBOL, CATEGORY_ATTRIBUTE:"BLA2"}), \
    A({KIND_ATTRIBUTE: URL_SYMBOL, STRING_ATTRIBUTE: "www.blebu.pl", CATEGORY_ATTRIBUTE:"BLA3"}), \
    A({KIND_ATTRIBUTE: PUNCTUATION_SYMBOL, STRING_ATTRIBUTE: RT_SYMBOL, CATEGORY_ATTRIBUTE:"BLA4"}), \
    A({KIND_ATTRIBUTE: STRING_ATTRIBUTE, STRING_ATTRIBUTE: "@MaryJane", CATEGORY_ATTRIBUTE:"BLA5"})])
    [',', 'RT', '@MaryJane']
    '''
    res = []
    #prev_hash = False
    prev_rt = False
    #global cnt
    for child in children:
        if child.attrib[KIND_ATTRIBUTE] != URL_SYMBOL and \
        child.attrib[STRING_ATTRIBUTE] != HASHTAG_SYMBOL and \
        child.attrib[STRING_ATTRIBUTE] != AT_SYMBOL and \
        child.attrib[STRING_ATTRIBUTE] != RT_SYMBOL:
            #if not prev_hash and not prev_rt:
            if lower:
                if not prev_rt and type(child.attrib[STRING_ATTRIBUTE])==str:
                    res.append(child.attrib[STRING_ATTRIBUTE].lower())
            else:
                res.append(child.attrib[STRING_ATTRIBUTE])
            #update info about if it is a hashtag: 
            #prev_hash = (child.attrib[KIND_ATTRIBUTE] == PUNCTUATION_SYMBOL and \
            #         child.attrib[STRING_ATTRIBUTE] == HASHTAG_SYMBOL)
            #update info about if it is an rt:
        prev_rt = child.attrib[STRING_ATTRIBUTE] == RT_SYMBOL
    return res

def bigrams(unigrams):
    return nltk.bigrams(unigrams)

if __name__ == "__main__":
    import doctest
    doctest.testmod()
