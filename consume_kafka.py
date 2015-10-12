import json
from pykafka import KafkaClient
from add_misinformation_to_json import process_jsons
client = KafkaClient(hosts="127.0.0.1:9092")
topic=client.topics['TutorialTopic']

consumer = topic.get_simple_consumer()

for msg in consumer:
    if msg is not None:
        print msg.offset, msg.value
        try:
            json.loads(msg)
            res=process_jsons([json.loads(msg)])
            print "postprocessed:", msg
        except:
            print "something went wrong!"
