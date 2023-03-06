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
    
    multi_polygon=shape(fake.multipolygon()).wkt
    polygon=shape(fake.polygon()).wkt
    point=shape(fake.point()).wkt

    print(json.dumps({
        "tsString": ts, 
        "uuid": id, 
        "count": count, 
        "polygonString": polygon,
        "multiPolygonString": multi_polygon,
        "pointString": point
    }))
