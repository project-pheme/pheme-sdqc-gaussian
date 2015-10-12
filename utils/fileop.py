'''
Created on 28 Nov 2013

@author: michal
'''
import os
def for_fullfile_in_cat(catname):
    '''
    Yields files from catname one by one.
    '''
    for fname in os.listdir(catname):
        fullpath = os.path.join(catname,fname)
        if os.path.isfile(fullpath):
            yield fullpath, fname

def ensure_dir(f):
    '''
    Checks if catalogue f exists, if not then creates it
    '''
    d = os.path.dirname(f)
    if not os.path.exists(d):
        os.makedirs(d)


REPLACING_BACKSHLASH = ""
def convert_url2fname(url):
    return url.replace("/", REPLACING_BACKSHLASH)