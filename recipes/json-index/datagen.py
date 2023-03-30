from faker import Faker
import json
import datetime as dt
import click
import time
from decimal import Decimal
import random

fake = Faker()

class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        return float(obj) if isinstance(obj, Decimal) else super().default(obj)

INTERESTS = ['Music', 'Sports', 'Reading', 'Cooking', 'Traveling', 'Hiking', 'Art', 'Dancing',
             'Photography', 'Gardening', 'Fashion', 'Baking', 'Cycling', 'Swimming', 'Fishing',
             'Skiing', 'Running', 'Yoga', 'Meditation', 'Painting']

def generate_person():
    current_person = {}
    current_person['id'] = fake.uuid4()
    current_person['name'] = fake.name()
    current_person['email'] = fake.email()
    current_person['age'] = fake.random_int(min=18, max=80)
    current_person['address'] = {
        'street_address': fake.street_address(),
        'city': fake.city(),
        'state': fake.state(),
        'country': fake.country()
    }
    current_person['phone_number'] = fake.phone_number()
    current_person['job'] = {
        'company': fake.company(),
        'position': fake.job(),
        'department': fake.bs()
    }
    current_person['interests'] = random.choices(INTERESTS, k=random.randint(1, 5)) if random.randint(0,10) > 1 else None
    current_person['friend_ids'] = [fake.uuid4() for _ in range(random.randint(1, 3))] if random.randint(0,10) > 1 else None
    return current_person

@click.command()
@click.option('--sleep', default=0.0, help='Sleep between each message')
def generate_data(sleep):
    while True:
        current_data = {}
        current_data['ts'] = int(dt.datetime.now().timestamp() * 1000)
        current_data['person'] = generate_person()
        print(json.dumps(current_data, indent=4, cls=DecimalEncoder))
        time.sleep(sleep)

if __name__ == '__main__':
    while True:
        generate_data()
