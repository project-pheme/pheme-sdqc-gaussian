import json
from pykafka import KafkaClient
import sys  

topicname=sys.argv[1]#'TutorialTopic'

client = KafkaClient(hosts="127.0.0.1:9092")
topic=client.topics[topicname]

fin = sys.stdin
jsons=json.loads(fin.readline())

with topic.get_producer() as producer:
    for i in fin.xreadlines():
        producer.produce(i)
