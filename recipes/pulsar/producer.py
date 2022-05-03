import pulsar
import json
import time
import random
import uuid

client = pulsar.Client('pulsar://localhost:6650')
producer = client.create_producer('events')

while True:
    message = {
        "ts": int(time.time() * 1000.0),
        "uuid": str(uuid.uuid4()).replace("-", ""),
        "count": random.randint(0, 1000)
    }
    payload = json.dumps(message, ensure_ascii=False).encode('utf-8')
    producer.send(payload)

client.close()