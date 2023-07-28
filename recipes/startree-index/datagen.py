
import datetime
import uuid
import random
import json
from faker import Faker
fake = Faker()

pageIDs = [f'page{str(i).zfill(3)}' for i in range(1, 101)]  # Generating 100 page IDs
device_types = ['Desktop', 'Laptop', 'Mobile', 'Tablet']
device_brands = ['Apple', 'Dell', 'Samsung', 'Lenovo', 'Huawei']
device_models = {
    'Desktop': ['iMac 2022', 'Dell XPS Desktop', 'HP Pavilion'],
    'Laptop': ['MacBook Pro', 'Dell XPS 15', 'Lenovo ThinkPad X1'],
    'Mobile': ['iPhone 13', 'Samsung Galaxy S21', 'Google Pixel 6'],
    'Tablet': ['iPad Pro', 'Samsung Galaxy Tab S7', 'Surface Pro X']
}
browser_types = ['Chrome', 'Firefox', 'Safari', 'Edge', 'Opera']
browser_versions = {
    'Chrome': ['90.0.4430.93', '91.0.4472.124', '92.0.4515.159'],
    'Firefox': ['89.0.1', '90.0.2', '91.0.2'],
    'Safari': ['13.1.2', '14.0.3', '15.0'],
    'Edge': ['91.0.864.59', '92.0.902.78', '93.0.961.52'],
    'Opera': ['76.0.4017.177', '77.0.4054.277', '78.0.4093.147']
}
locales = ['en_US', 'fr_FR', 'de_DE', 'es_ES', 'zh_CN']


while True:
    ts = int(datetime.datetime.now().timestamp() * 1000)
    user_id = str(uuid.uuid4())
    time_spent = random.randint(5, 1200)  # Time spent on a page in seconds
    pageID = random.choice(pageIDs)
    country = fake.country()
    device_type = random.choice(device_types)
    device_brand = random.choice(device_brands)
    device_model = random.choice(device_models[device_type])
    browser_type = random.choice(browser_types)
    browser_version = random.choice(browser_versions[browser_type])
    locale = random.choice(locales)

    event = {
        "ts": ts,
        "userID": user_id[:8],  # For privacy, only taking first 8 characters of UUID
        "timeSpent": time_spent,
        "pageID": pageID,
        "country": country,
        "deviceType": device_type,
        "deviceBrand": device_brand,
        "deviceModel": device_model,
        "browserType": browser_type,
        "browserVersion": browser_version,
        "locale": locale
    }

    print(
        json.dumps(event)
    )
