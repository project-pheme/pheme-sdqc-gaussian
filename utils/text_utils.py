# -*- coding: utf-8 -*-
'''
Created on 1 Jun 2015

@author: michal
'''
import re
import string
punct = string.punctuation

PUNCTUATION_IRRELEVANT = set(string.punctuation)
PUNCTUATION_IRRELEVANT.add(u"«")
PUNCTUATION_IRRELEVANT.add(u"“")
PUNCTUATION_IRRELEVANT.add(u"”")
PUNCTUATION_SET_ALL=PUNCTUATION_IRRELEVANT.copy()

PUNCTUATION_IRRELEVANT.remove("?")
PUNCTUATION_IRRELEVANT.remove("!")
PUNCTUATION_IRRELEVANT.remove(".")

PUNCTUATION_SPLITBY_rePATTERNS=['(\?)','(\!)', '(\.)']


#source: http://library.blackboard.com/ref/a47a6afa-c957-4711-979b-975ff747de1d/content/moderators_and_participants_guides/appendices/appendix_emoticons.htm
# plus a little from me: :o, :|, =/, :s, :S, :p
EMOTICON2STRING = { 
                    ":)": "Smile",
                    ":-)": "Smile",
                    ";)": "Wink",
                    ";-)": "Wink",
                    ":(": "Sad",
                    ":-(": "Sad",
                    "(re)": "Eye",
                    "B)": "Cool",
                    "B-)": "Cool",
                    ":s": "Grim",#
                    ":S": "Grim",#
                    ":p": "Tongue",#
                    ":-P": "Tongue",
                    "d:": "Tongue",
                    ":O": "Surprised",
                    ":-O": "Surprised",
                    ":'(": "Crying",
                    ":/": "Confused",
                    "=/": "Confused",
                    ":-/": "Confused",
                    ":D": "Grin",
                    ":-D": "Grin",
                    ":@": "Angry",
                    ":-@": "Angry",
                    "(6)": "Evil",
                    ":*": "Kiss",
                    ":-*": "Kiss",
                    "<3": "Heart",
                    "</3": "Broken",
                    "(shazam)": "Lightening",
                    "(p)": "Report",
                    "(e)": "Email",
                    "(s)": "Open",
                    "(ns)": "Book",
                    "(#)": "Chart",
                    "(+)": "Clock",
                    "(c)": "Coffee",
                    "(hb)": "Birthday",
                    "(t)": "Telephone",
                    "(tv)": "Television",
                    "(m)": "Music",
                    "(01)": "Computer",
                    "(i)": "iPod",
                    "(g)": "Game",
                    "(w)": "Webcam",
                    ":[": "Bat",
                    "(z)": "Man",
                    "(x)": "Woman",
                    "(f)": "Group",
                    "(cc)": "Credit",
                    "($)": "Money",
                    "(!)": "Alert",
                    "(eye)": "Eye",
                    "(a)": "Car",
                    "(xy)": "Male",
                    "(xx)": "Female",
                    "(1)": "Soccer",
                    "(2)": "Football",
                    "(3)": "Basketball",
                    "(8)": "8",
                    "(h)": "House",
                    "(zz)": "Sleep",
                    "(n)": "Thumbs",
                    "(y)": "Thumbs",
                    "(su)": "Sun",
                    "(ts)": "Cloud",
                    "(rn)": "Rain",
                    "(sn)": "Snow",
                    "(r)": "Rainbow",
                    "(*)": "Star",
                    ":o": "Surprised",
                    ":|": "Dissapointed"}

def is_emoticon(x):
    return x in EMOTICON2STRING

def lookup_emoticon(x):
    if is_emoticon(x):
        return EMOTICON2STRING[x]
    return x

def split_by_keeping(tmp_field, split_by_set):
    '''
    >>> split_by_keeping(["eb", "ble", "ebuebu"], ['e'])
    ['e', 'b', 'bl', 'e', 'e', 'bu', 'e', 'bu']
    >>> split_by_keeping(["eb", "ble", "ebuebu", "ebuebue"], ['e'])
    ['e', 'b', 'bl', 'e', 'e', 'bu', 'e', 'bu', 'e', 'bu', 'e', 'bu', 'e']
    '''
    for punct_re in split_by_set:
        tmp_res = []
        for w in tmp_field:
            res=w.split(punct_re)#map(str, re.split(punct_re, w))
            
            res2=[]
            for i in range(2*len(res)-1):
                if i%2==0:
                    res2.append(res[i/2])
                else:
                    res2.append(punct_re)
            #print "res2:", res2
            tmp_res+=res2
        tmp_field = tmp_res
    return filter(lambda x: x, tmp_field)


def split_by_deleting(tmp_field, split_by_set):
    '''
    >>> split_by_deleting(["eb", "ble", "ebuebu"], ['e'])
    ['b', 'bl', 'bu', 'bu']
    >>> split_by_deleting(["eb", "ble", "ebuebu", "ebuebue"], ['e'])
    ['b', 'bl', 'bu', 'bu', 'bu', 'bu']
    '''
    for punct_sign in split_by_set:
        tmp_res = []
        for w in tmp_field:
            tmp_res += w.split(punct_sign)
        tmp_field = tmp_res
    return filter(lambda x: x, tmp_field)

if __name__ == "__main__":
    import doctest
    doctest.testmod()