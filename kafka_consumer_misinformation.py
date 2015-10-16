#!/usr/bin/env python
'''

Example arguments: #test1 test2 data/twoPHEME_datasets_as_events_041015.csv results/store_models_test/BROWNGPjoinedfeaturesPooledLIN0.pick
'''
import json, sys
from pykafka import KafkaClient
from add_misinformation_to_json import process_jsons
import pickle
import os
FILE_TMP="file_tmp.txt"
FILE_TMP2="file_tmp2.txt"

#topicin="test1"#sys.argv[1]
#topicout="test2"#sys.argv[2]
#trainingdatapath="data/twoPHEME_datasets_as_events_041015.csv"#sys.argv[3]
#modelpath="results/store_models_test/BROWNGPjoinedfeaturesPooledLIN0.pick"#sys.argv[4]
topicin=sys.argv[1]
topicout=sys.argv[2]
trainingdatapath=sys.argv[3]
modelpath=sys.argv[4]

header=open(trainingdatapath).readline().split()
m=pickle.load(open(modelpath, "r"))
client = KafkaClient(hosts="127.0.0.1:9092")
consumer = client.topics[topicin].get_simple_consumer()

with client.topics[topicout].get_producer() as producer:
    for msg in consumer:
        if msg is not None:
            msgval = unicode(json.loads(msg.value)['tweet']['rawJson'])
	    if json.loads(msgval)['lang'] != 'en':
              continue
            with open(FILE_TMP2, 'w') as ftmp:
                try:
                    ftmp.write(msgval)
                except:
                    continue
            command="cat "+FILE_TMP2+" | python text.py -t txt -r text -p 19,0,15,5,3,6,4,20,8 -w BROWN_STR -b data/resources/50mpaths2 -j lines > "+FILE_TMP
            os.system(command)
            with open(FILE_TMP, 'r') as ftmp:
                augmented=ftmp.readline()
            for res in process_jsons([json.loads(augmented)], header, m):
                # print "Added misinformation to a json, resulting in the following json:", res
                print msg.partition.id, msg.offset, res['pheme_sdqc'], json.loads(augmented)[0]['text'][:100]
                producer.produce(json.dumps(res))
