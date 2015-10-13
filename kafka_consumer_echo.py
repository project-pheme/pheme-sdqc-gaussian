import json, sys
from pykafka import KafkaClient
from add_misinformation_to_json import process_jsons

topicin=sys.argv[1]

client = KafkaClient(hosts="127.0.0.1:9092")
topic=client.topics[topicin]
consumer = topic.get_simple_consumer()


for msg in consumer:
    if msg is not None:
        print msg.offset, msg.value