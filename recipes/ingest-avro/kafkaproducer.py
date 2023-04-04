import json
import sys
from confluent_kafka import Producer, KafkaException
from confluent_kafka.avro import AvroProducer
from confluent_kafka import avro


def acked(err, msg):
    if err is not None:
        print('Failed to deliver message: %s: %s' % msg.value().decode('utf-8'), str(err))
    else:
        print('Message produced: %s' % msg.value().decode('utf-8'))


def kafka_producer(schema_name="mastodon-topic"):
    producer_config = {
        'bootstrap.servers': 'localhost:9092',
        'schema.registry.url': 'http://localhost:8081', 
        'broker.address.family': 'v4'
    }

    value_schema = avro.load(f"avro/{schema_name}-value.avsc")
    producer = AvroProducer(producer_config, default_value_schema=value_schema)
    return schema_name, producer

if __name__ == "__main__":
    topic_name, producer = kafka_producer(schema_name="person-topic")

    while True:
        line = sys.stdin.readline().rstrip('\n')
        if not line:
            break
        event = json.loads(line)
        producer.produce(topic = topic_name, value = event)
        producer.flush()

    
    # producer.produce(topic = topic_name, value = value_dict)
    # producer.flush()
