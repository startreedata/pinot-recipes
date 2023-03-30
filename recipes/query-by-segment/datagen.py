import datetime as dt
import uuid
import random
import json

while True:
    ts = int(dt.datetime.now().timestamp() * 1000)
    id = str(uuid.uuid4())
    count = random.randint(0, 1000)
    print(
        json.dumps({"tsString": ts, "uuid": id, "count": count})
    )
