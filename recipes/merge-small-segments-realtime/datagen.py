import datetime as dt
import uuid
import random
import json
import time

while True:
    now = dt.datetime.now()
    ts = int(now.timestamp() * 1000)
    id = str(uuid.uuid4())
    count = random.randint(0, 1000)
    print(
        json.dumps({"ts": ts, "uuid": id, "count": count})
    )

    sleep_time = 0.01 if now.minute % 2 == 0 else 0.00005
    time.sleep(sleep_time)
