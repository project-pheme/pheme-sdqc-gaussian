'''
Created on 12 Oct 2015

@author: michal

This script assumes that the only features used is Brown clusters.

Example json for tests:

jsons=[{"contributors":None,"truncated":False,
   "text":"\u201c@flavius217: It appears that #Ferguson PD are trying to assassinate Mike Brown's character after literally assassinating Mike Brown.\u201d",
   "in_reply_to_status_id":500307001629745152,"id":500315576460668929,"favorite_count":0,"source":"<a href=\"http:\/\/twitter.com\/download\/iphone\" rel=\"nofollow\">Twitter for iPhone<\/a>","retweeted":False,"coordinates":None,
   "entities":{"symbols":[],"user_mentions":[{"id":59042511,"indices":[1,12],"id_str":"59042511","screen_name":"flavius217","name":"Jeff"}],
               "hashtags":[{"indices":[30,39],"text":"Ferguson"}],"urls":[]},"in_reply_to_screen_name":"flavius217","id_str":"500315576460668929","retweet_count":0,
   "in_reply_to_user_id":59042511,"favorited":False,
   "user":{"follow_request_sent":False,"profile_use_background_image":True,"default_profile_image":False,
                                                            "id":102177639,"profile_background_image_url_https":"https:\/\/pbs.twimg.com\/profile_background_images\/532290446\/gold-water.jpg","verified":False,"profile_text_color":"0A0101","profile_image_url_https":"https:\/\/pbs.twimg.com\/profile_images\/535657643495653376\/YB-oy4fF_normal.jpeg","profile_sidebar_fill_color":"F5EBEB","entities":{"url":{"urls":[{"url":"http:\/\/t.co\/4WX84gMfiJ","indices":[0,22],"expanded_url":"http:\/\/jadillaphotography.tumblr.com","display_url":"jadillaphotography.tumblr.com"}]},                                                                                                                                                                                                                                                                                                                                                                                                    "description":{"urls":[]}},"followers_count":559,"profile_sidebar_border_color":"F20909","id_str":"102177639","profile_background_color":"0F0202","listed_count":0,
           "is_translation_enabled":False,"utc_offset":-28800,"statuses_count":18973,
           "description":"#TPH Follow my bestest friend @galiblaaahd Photographer for Creative Revolution Union IG: Jadillaa RIP Andy #DRO Avin",
           "friends_count":488,"location":"I stays in the Nutty ","profile_link_color":"FA141F",
           "profile_image_url":"http:\/\/pbs.twimg.com\/profile_images\/535657643495653376\/YB-oy4fF_normal.jpeg",
           "following":False,"geo_enabled":False,"profile_banner_url":"https:\/\/pbs.twimg.com\/profile_banners\/102177639\/1353685233",
           "profile_background_image_url":"http:\/\/pbs.twimg.com\/profile_background_images\/532290446\/gold-water.jpg","screen_name":"Jadeezzyy",
           "lang":"en","profile_background_tile":True,"favourites_count":1732,"name":"JADILLA",
           "notifications":False,"url":"http:\/\/t.co\/4WX84gMfiJ","created_at":"Tue Jan 05 21:59:27 +0000 2010",
           "contributors_enabled":False,"time_zone":"Alaska","protected":False,"default_profile":False,"is_translator":False},"geo":None,"in_reply_to_user_id_str":"59042511","lang":"en","created_at":"Fri Aug 15 16:18:23 +0000 2014","in_reply_to_status_id_str":"500307001629745152","place":None,
           "BROWN_STR": {"111001111": 3, "111001110": 2, "0111100111111": 1, "01011011111110": 1, "0111100011100": 1, "001011111010": 1, "11100100": 1, "1110010101": 1, "1111011110111110": 1, "01110110": 1, "01101111110100": 1, "111010110100": 1}
        }
]
'''
import sys
import numpy as np
import pickle
import GPy
import json
def map_to_string_label(lbl):
    if lbl==11:
        return "support"
    if lbl==12:
        return "deny"
    if lbl==13:
        return "question"
    if lbl==14:
        return "comment"
def process_jsons(jsons, header, m):
    for j in jsons:
        X=np.zeros((1, len(header)))
        for indh, valh in enumerate(header):
            if "BROWN_STR" not in valh:
                continue
            browncluster=valh.split("_")[2]
            if browncluster in j["BROWN_STR"]:
                X[0,indh]=j["BROWN_STR"][browncluster]
        misinfo, results_dict=m.predict_certainty(X)
        j["pheme_sdqc"]=(map_to_string_label(misinfo[0]), (results_dict[misinfo[0]]/np.sum(results_dict.values())).flatten()[0])
        j.pop("BROWN_STR", None)
        yield j
if __name__=="__main__":
    #Arguments for the script: trained model and training set used to train that model:
    modelpath=sys.argv[1]
    trainingdatapath=sys.argv[2]#"data/twoPHEME_datasets_as_events_041015.csv"
    outputfile=sys.argv[3]#"kafka_out.txt"
    
    #format: Brown clusters from X; timestamp event is_simple_retweet is_complex_retweet id support
    header=open(trainingdatapath).readline().split()
    m=pickle.load(open(modelpath, "r"))
    fin = sys.stdin
    jsons=json.loads(fin.readline())
    fout=open(outputfile, 'w')
    json.dump(list(process_jsons(jsons, header, m)), fout)
