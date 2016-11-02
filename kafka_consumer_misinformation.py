#!/usr/bin/env python
'''

Example arguments: #test1 test2 data/twoPHEME_datasets_as_events_041015.csv results/store_models_test/BROWNGPjoinedfeaturesPooledLIN0.pick
'''
import json, sys
from pykafka import KafkaClient
from add_misinformation_to_json import process_jsons
import pickle
import os
import time
FILE_TMP=str(os.getpid())+"_a.tmp"
FILE_TMP2=str(os.getpid())+"_b.tmp"

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
client = KafkaClient(hosts="gatezkt1.storm:9092")
consumer = client.topics[topicin].get_simple_consumer(consumer_group="sdqc")

print time.strftime('%c'), 'starting'

with client.topics[topicout].get_producer() as producer:
    for msg in consumer:
        if msg is not None:
            try:
                msgval = json.loads(msg.value)
            except:
                print('bad json')
                print(msg.value)
                continue
#            if msgval['lang'] != 'en':
#                continue
#            print('Processing', msgval['id'])
            with open(FILE_TMP2, 'w') as ftmp:
                try:
                    ftmp.write(json.dumps(msgval))
                except Exception, e:
                    print('Failed to write to', FILE_TMP2)
                    print(e)
                    continue
            command="cat "+FILE_TMP2+" | ~/sdqc2/bin/python2 text.py -t txt -r text -p 19,0,15,5,3,6,4,20,8 -w BROWN_STR -b data/resources/50mpaths2 -j lines > "+FILE_TMP
            os.system(command)
            with open(FILE_TMP, 'r') as ftmp:
                augmented=ftmp.readline()

            try:
                j = json.loads(augmented)
            except:
                print('Failed to load augmented JSON:')
                print(augmented)
                sys.exit()

            for res in process_jsons(j, header, m):
                # print "Added misinformation to a json, resulting in the following json:", res
                print time.strftime('%c'), msg.partition.id, msg.offset, res['pheme_sdqc'], json.loads(augmented)[0]['text'][:100]
                producer.produce(json.dumps(res))
