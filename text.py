#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 15 Jul 2014

@author: michal

- Modifies text from the input field and puts the result to the otput field
- The method for reading the tokens from the field is specified in the WORDS_EXTRACTOR function at the top of this script
- The method for outputting is also below

Example usage (when read from stdin):
python text.py -r gatexml -p 5,3,6,2,4,9,10,8 -t xmltxt -w BOW_STR
'''
import sys
import json
import parse_feats.token_extraction
from parse_feats.token_extraction import STOPWORDS_SET
from optparse import OptionParser
from collections import Counter
import nltk
from nltk.stem.porter import PorterStemmer
from nltk.stem.snowball import EnglishStemmer
from utils.constants import *
from utils.spectral import parse_spectral_cluster_dictionary
from nltk.stem import WordNetLemmatizer
import re
from utils.text_utils import lookup_emoticon, PUNCTUATION_SPLITBY_rePATTERNS, is_emoticon, PUNCTUATION_SET_ALL,\
    PUNCTUATION_IRRELEVANT, EMOTICON2STRING, split_by_deleting, split_by_keeping
import sklearn
import sklearn.metrics

#taken from: http://stackoverflow.com/questions/6883049/regex-to-find-urls-in-string-in-python
LINK_REG = 'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
LINK_PLACEHOLDER = "URLPLACEHOLDER"
                    

def hasNumbers(inputString):
    return any(char.isdigit() for char in inputString)

FILTER_OUT = lambda child: child.text.startswith("@") or child.text.startswith("#") or child.attrib[parse_feats.token_extraction.CATEGORY_ATTRIBUTE]=='nnp'

WORDS_EXTRACTOR_XML = lambda x: parse_feats.token_extraction.strings_children(x, FILTER_OUT)
#WORDS_EXTRACTOR_TXT = nltk.word_tokenize 
WORDS_EXTRACTOR_TXT = nltk.wordpunct_tokenize

WORDS_EXTRACTOR_XML_POS = lambda x: parse_feats.token_extraction.poss_children(x, FILTER_OUT)

if __name__ == '__main__':
    #"""
    usage = "usage: %prog [options] arg"
    parser = OptionParser(usage)
    parser.add_option("-i", "--input", dest="infile_name",
                      help="path to input JSON file, if none specified then stdin is read")
    parser.add_option("-r", "--read", dest="input_field",
                      help="what field to read")
    parser.add_option("-t", "--type", dest="type_of_input_field",
                      help="what type of an input field: txt or xmltxt or xmlpos")
    parser.add_option("-j", "--jsonloadtype", dest="jsonloadtype",
                      help="json load type: as one json (default) or as list of jsons per line (lines)")
    parser.add_option("-o", "--output", dest="outfile_name",
                      help="path to output JSON file, if none specified then redirection to stdout")
    parser.add_option("-w", "--write", dest="output_field",
                      help="what field to output")
    parser.add_option("-d", "--dictionary", dest="scdict",
                      help="path to a spectral clusters dictionary")
    parser.add_option("-p", "--options", dest="options",
                      help= "what tasks are to be consecutively done, comma seperated.\n"+\
                            "0 for splitting the string into tokens (useful to apply functions operating on different type of data\n"+\
                            "1 for filtering punctuation\n"+\
                            "2 for stemming\n"+\
                            "3 for stopwords removal\n"+\
                            "4 for lowercasing\n"+\
                            "5 for splitting words by '-' and '_'\n"+\
                            "6 for replacing emoticons with predefined strings\n"+\
                            "7 for bigram creation\n"+\
                            "8 for storing the counts\n"+\
                            "9 for replacing multiple occurences of a letter in a word by a double occurence\n"+\
                            "10 for removing non-ASCII characters\n"+\
                            "11 for adding the field required by the spectral clustering code implemented by Daniel P., e.i. \"analysis\": {\"tokens\": {\"all\": list of words\n"+\
                            "12 for adding the scores for clusters, from the dictionary passed in the field as  -d path2dictionary \n"+\
                            "13 for removing @ (and subsequent string) and # signs \n"+\
                            "14 for removing punctuation \n"+\
                            "15 for removing URLs using a heuristic \n"+\
                            "16 for removing strings containing digits \n"+\
                            "17 for Snowball stemming \n"+\
                            "18 for Wordnet lemmatizer \n"+\
                            "19 for replacing URLs with placeholders (USE BEFORE 0)\n"+\
                            "20 for replacing words with Brown clusters (requires specifying path to the dictionary)\n"+\
                            "21 for replacing words with all levels of Brown clusters that they belong to (requires specifying path to the dictionary)\n"+\
                            "22 for keeping only punctuation\n"+\
                            "23 for keeping only emoticons\n"+\
                            "24 for keeping only hashtags\n"+\
                            "25 for keeping only URL placeholder\n"+\
                            "26 for keeping only the user name in text\n"+\
                            "27 for classifying for www2015 regex for questioning and rejecting labels")
    parser.add_option("-k", "--keywords", action="store_true", dest="output_keywords",
                      help="should the keywords be printed at the end of the processing. In such case, the JSONs are not outputted.")
    parser.add_option("-b", "--brownclusters", dest="brownclusters",
                      help="path to brown clusters dictionary.")
    
    (parser_options, parser_args) = parser.parse_args()
    
    if parser_options.options != None:
        options = map(int, parser_options.options.split(","))
    
    if parser_options.infile_name != None:
        fin = open(parser_options.infile_name, 'r')
    else:
        fin = sys.stdin
    
    if parser_options.outfile_name != None:
        fout = open(parser_options.outfile_name, 'w')
    else:
        fout = sys.stdout
    #"""
    
    """
    fin=open("../../../../qazvinian/data/intermediatelondonriots_BOW.json")#army_bank.json")
    class empty(object):
        pass
    parser_options=empty()
    options=[0, 4, 27]#[19,0,6,15,5,4,3,20,8]#[0, 22]#[19,0,6,15,5,4,9,10,13,14,16,3,18,8]
    parser_options.store_results=False
    parser_options.type_of_input_field='txt'
    parser_options.input_field='body'
    parser_options.output_field='BOW_STR'
    parser_options.brownclusters=None
    parser_options.jsonloadtype=None
    parser_options.emoticon_field="EMOTICON"
    #keys2delete=[]
    """
    
    brownclusters_dict = {}
    if parser_options.brownclusters != None:
        with open(parser_options.brownclusters, 'r') as f:
            for line in f:
                l = line.replace("\n", "").split("\t")
                brownclusters_dict[l[1]] = l[0]

    if parser_options.type_of_input_field == None:
        print "Type of input field required"
        sys.exit(-1)
    elif parser_options.type_of_input_field == "xmltxt":
        WORDS_EXTRACTOR = WORDS_EXTRACTOR_XML
    elif parser_options.type_of_input_field == "txt":
        WORDS_EXTRACTOR = WORDS_EXTRACTOR_TXT
    elif parser_options.type_of_input_field == "xmlpos":
        WORDS_EXTRACTOR = WORDS_EXTRACTOR_XML_POS
    else:
        print "Unknown type of input field"
        sys.exit(-1)
    
    if parser_options.jsonloadtype=="lines":
        jsons=[json.loads(x) for x in fin.xreadlines()]
    else:
        jsons = json.load(fin)
    #print "jsons:", jsons
    
    #lists used by option 27 for classifying for www2015 regex for questioning and rejecting labels
    predq=[]
    trueq=[]
    predr=[]
    truer=[]
    all_lbls=[]
    
    for jind, j in enumerate(jsons):
        #print "j:", j
        if parser_options.type_of_input_field != "txt":
            try:
                j[JSON_FIELD_TOKENS] = parse_feats.token_extraction.xml_tokens(j[parser_options.input_field], from_file=False)
            except:
                #in case it is read from the input stream, encode has to be done:
                j[JSON_FIELD_TOKENS] = parse_feats.token_extraction.xml_tokens(j[parser_options.input_field].encode('utf8'), from_file=False)
        else:
            j[JSON_FIELD_TOKENS] = j[parser_options.input_field]
        
        for option in options:
            if option==0:
                tmp_field = WORDS_EXTRACTOR(j[JSON_FIELD_TOKENS])#[parser_options.input_field])
                tmp_field = filter(lambda x: x!='' and x!="" and x!=' ' and x, tmp_field)
            
            if option==1:
                tmp_field = filter(lambda x: x not in PUNCTUATION_IRRELEVANT, tmp_field)
            
            if option==2:
                #Create a new Porter stemmer.
                stemmer = PorterStemmer()
                tmp_field = map(stemmer.stem, tmp_field)
            
            if option==3:
                tmp_field = filter(lambda x: x not in STOPWORDS_SET, tmp_field)
            
            if option==4:
                tmp_field = map(lambda x: x.lower(), tmp_field)
            
            if option==5:
                tmp_res = []
                for w in tmp_field:
                    wl = w.split() 
                    wl = reduce(lambda a, b: a+b, map(lambda x: x.split("-"), wl))
                    wl = reduce(lambda a, b: a+b, map(lambda x: x.split("_"), wl))
                    tmp_res += wl
                tmp_field = tmp_res
                
            if option==6:
                tmp_field = map(lookup_emoticon, tmp_field)
            
            if option==23:
                tmp_field=filter(lambda x: is_emoticon(x), tmp_field)
                tmp_field = map(lookup_emoticon, tmp_field)
            
            if option==7:
                tmp_field = map(lambda x: str(x[0])+"_"+str(x[1]), nltk.bigrams(tmp_field))
            
            if option==8:                    
                tmp_field = filter(lambda x: x!='' and x!="" and x!=' ' and x, tmp_field)
                j[parser_options.output_field] = dict(Counter(tmp_field))
                
            if option==9:
                def collapse(s):
                    if len(s) <= 2:
                        return s
                    l = list(s)
                    lout = [l[0], l[1]]
                    for i in xrange(2,len(l)):
                        if not(l[i]==l[i-1]==l[i-2]):
                            lout.append(l[i])
                    return ''.join(lout)
                        
                tmp_field = map(lambda x: collapse(x), tmp_field)
            
            if option==10:
                def remove_non_ascii_1(text):
                    return ''.join(i for i in text if ord(i)<128)
                
                tmp_field = map(lambda x: remove_non_ascii_1(x), tmp_field)
            
            if option==11:
                j["analysis"] = {}
                j["analysis"]["tokens"] = {}
                j["analysis"]["tokens"]["all"] = tmp_field
            
            if option==12:
                
                scdict = parse_spectral_cluster_dictionary(parser_options.scdict)
                spc_dict = {}
                for w in tmp_field:
                    try:
                        spc_dict[scdict[w][0]] = spc_dict.get(scdict[w][0], 0) + scdict[w][1]
                    except KeyError:
                        pass
                j[SPECTRAL_CLUSTER_FIELD] = spc_dict
            
            if option==13:
                #remove all @ signs together with subsequent string
                while '@' in tmp_field:
                    ind = tmp_field.index('@')
                    tmp_field = tmp_field[:ind]+tmp_field[ind+2:]
                tmp_field = filter(lambda x: x!='#', tmp_field)
        
            #delete punctuation:
            if option==14:
                if len(tmp_field) > 0:
                    #tmp_field=split_by_deleting(tmp_field, PUNCTUATION_IRRELEVANT)
                    #tmp_field=split_by_keeping(tmp_field, PUNCTUATION_SPLITBY_rePATTERNS)
                    tmp_field=split_by_deleting(tmp_field, PUNCTUATION_SET_ALL)
            #keep only punctuation:
            if option==22:
                if len(tmp_field) > 0:
                    tmp_field=split_by_keeping(tmp_field, PUNCTUATION_SET_ALL)
                    tmp_field=filter(lambda x: x in PUNCTUATION_SET_ALL, tmp_field)
            
            if option==15:
                tmp_field = filter(lambda x: "/" not in x and "http" not in x and ":" not in x, tmp_field)
                
            if option==16:
                tmp_field = filter(lambda x: not hasNumbers(x), tmp_field)
            
            if option==17:
                stemmer = EnglishStemmer()
                tmp_field = map(stemmer.stem, tmp_field)
                
            if option==18:
                wnl = WordNetLemmatizer()
                tmp_field = map(wnl.lemmatize, tmp_field)

            #URLS -> placeholder
            if option==19:
                j[JSON_FIELD_TOKENS] = re.sub(LINK_REG, LINK_PLACEHOLDER, j[JSON_FIELD_TOKENS])

            #25 for keeping only URL placeholder
            if option==25:
                tmp_field = filter(lambda x: x==LINK_PLACEHOLDER, tmp_field)

            if option==20:
                tmp_field = filter(lambda k: k in brownclusters_dict, tmp_field) 
                tmp_field = map(lambda k: brownclusters_dict[k], tmp_field)
            
            if option==21:
                tmp_field = filter(lambda k: k in brownclusters_dict, tmp_field) 
                tmp_field = map(lambda k: brownclusters_dict[k], tmp_field)
                tmp_field = reduce(lambda x, y: x+y, map(lambda x: [x[:i] for i in xrange(1, len(x)+1)], tmp_field))
                
            #24 for keeping only hashtags
            if option==24:
                import re
                tmp_field=map(lambda s: s.lower(), re.findall(r"#(\w+)", j[JSON_FIELD_TOKENS]))
                
            #26 for keeping only the user name in text
            if option==26:
                tmp_field=[j['author']]
            
            #27 for classifying for www2015 regex for questioning and rejecting labels
            if option==27:
                rejecting=[['rumour'], ['debunk']]
                for first in ['that', 'this', 'it']:
                    rejecting.append([first, 'is', 'not', 'true'])
                
                questioning=[['real', '?'], ['really', '?'], ['unconfirmed']]
                for first in ['that', 'this', 'it']:
                    questioning.append(['is', first, 'true'])
                for arep in range(10):
                    questioning.append(['wh'+'a'*arep+'t', '?', '!'])
                
                field_joined=" ".join(tmp_field)
                
                res=0
                for query in rejecting:
                    if " ".join(query) in field_joined:
                        res=1
                        break
                predr.append(res)
                
                if res==1:
                    1+1
                    if int(j['qtype']=='12'):
                        print "rejecting retrieved:", field_joined
                    
                res=0
                for query in questioning:
                    if " ".join(query) in field_joined:
                        res=1
                        break
                predq.append(res)
                
                if res==1:
                    1+1
                    if int(j['qtype']=='13'):
                        print "questioning retrieved:", field_joined
                
                trueq.append(int(j['qtype']=='13'))
                truer.append(int(j['qtype']=='12'))
                all_lbls.append(j['qtype'])
                
        del j[JSON_FIELD_TOKENS]
    
    if 27 in options:
        print Counter(all_lbls)
        print "Results questioning:"
        print sklearn.metrics.confusion_matrix(trueq, predq, labels=[0,1])
        print "precision:", sklearn.metrics.precision_score(trueq, predq, pos_label=1)
        print "recall:", sklearn.metrics.recall_score(trueq, predq, pos_label=1)
        print "sum(predq)", sum(predq)
        print "Results rejecting:"
        print sklearn.metrics.confusion_matrix(truer, predr, labels=[0,1])
        print "precision:", sklearn.metrics.precision_score(truer, predr, pos_label=1)
        print "recall:", sklearn.metrics.recall_score(truer, predr, pos_label=1)
        print "sum(predr)", sum(predr)
            
    #store results
    if parser_options.output_keywords:
        keywords = {}
        for j in jsons:
            for k in j[parser_options.output_field].keys():
                keywords[k] = keywords.get(k, 0)+j[parser_options.output_field][k]
        #keywords = sorted(filter(lambda x: len(x[0]) == 0 or x[0][0] !='@', keywords.items()), key=lambda x:x[0])
        keywords = sorted(keywords.items(), key=lambda x:x[0])
        print len(keywords), "Keywords:", keywords
    else:
        json.dump(jsons, fout)#, indent=1)
