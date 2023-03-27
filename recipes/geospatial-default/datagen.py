import datetime
import uuid
import random
import json
from faker import Faker
from geofactory import GeoFactory
from shapely.geometry import shape

fake = Faker()
fake.add_provider(GeoFactory)

while True:
    ts = int(datetime.datetime.now().timestamp() * 1000)
    id = str(uuid.uuid4())
    count = random.randint(0, 1000)
    
    try:
        point=shape(fake.point()).wkt

        print(json.dumps({
            "tsString": ts, 
            "uuid": id, 
            "count": count, 
            "pointString": point if random.randint(0, 10) > 1 else None
        }))
    except ValueError as err:
        pass
