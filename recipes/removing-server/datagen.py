import datetime as dt
import uuid
import random
import json

while True:
    ts = dt.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    id = str(uuid.uuid4())
    count = random.randint(0, 1000)
    print(
        json.dumps({"tsString": ts, "uuid": id, "count": count})
    )
