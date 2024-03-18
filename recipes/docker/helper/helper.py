#!/bin/local/python

import time, string
import random
import json, yaml, csv
import socket, requests
from urllib.parse import urlparse
import logging
import typer
from faker import Faker
from faker.providers import DynamicProvider
from difflib import SequenceMatcher
import pandas as pd
from confluent_kafka import Producer
from enum import Enum
from datetime import datetime

logger = logging.getLogger(__name__)
clock = ['|', '/', '-', '\\', '|', '/', '-', '\\']

class DataType(Enum):
    INT = 1
    INTEGER = INT
    STRING = 2
    DOUBLE = 3
    FLOAT = 33
    TIMESTAMP = 4
    DATE = 5
    TIME = 6
    LONG = 7
    BYTES = 8
    JSON = 9


class Column:
    def __init__(self, name:str, type:DataType=DataType.STRING) -> None:
        self.name = name
        self.type = type

    def __str__(self) -> str:
        return f'Column: {self.name} {self.type}'

class Schema():
    def __init__(self, name) -> None:
        self.name = name
        self.columns:dict[str, Column] = {}
        self.primary_keys:dict[str, Column] = {}

class PinotSchema(Schema):
    def __init__(self, schema_path:str) -> None:
        schema = json.load(open(schema_path))
        super().__init__(schema['schemaName'])
        self.schema = schema
        
        for dim in schema['dimensionFieldSpecs']:
            self.columns[dim['name']] = Column(
                name=dim['name'], 
                type=DataType[dim['dataType'].upper()]
            )

        if 'metricFieldSpecs' in schema:
            for metric in schema['metricFieldSpecs']:
                self.columns[metric['name']] = Column(
                    name=metric['name'], 
                    type=DataType[metric['dataType'].upper()]
                )
        
        if 'primaryKeyColumns' in schema:
            for key in schema['primaryKeyColumns']:
                self.primary_keys[key] = self.columns[key]

        if 'dateTimeFieldSpecs' in schema:
            for dt in schema['dateTimeFieldSpecs']:
                self.columns[dt['name']] = Column(
                    name=dt['name'], 
                    type=DataType[dt['dataType'].upper()]
                )


class Generator:
    def __init__(self, schema:Schema, limit:int=1000) -> None:
        self.schema = schema
        self.limit = limit
        self.cursor = 0
        Faker.seed(0)
        self.faker:Faker = Faker()
        self.__add_provider__(name='device_types', elements = ['Desktop', 'Laptop', 'Mobile', 'Tablet'])
        self.__add_provider__(name='device_brands', elements = ['Apple', 'Dell', 'Samsung', 'Lenovo', 'Huawei'])
        self.__add_provider__(name='device_models', elements = ['iMac 2022', 'Dell XPS Desktop', 'HP Pavilion',
                                                                'MacBook Pro', 'Dell XPS 15', 'Lenovo ThinkPad X1',
                                                                'iPhone 13', 'Samsung Galaxy S21', 'Google Pixel 6',
                                                                'iPad Pro', 'Samsung Galaxy Tab S7', 'Surface Pro X']
        )
        self.__add_provider__(name='browser_types', elements = ['Chrome', 'Firefox', 'Safari', 'Edge', 'Opera'])
        self.__add_provider__(name='browser_versions', elements = ['90.0.4430.93', '91.0.4472.124', '92.0.4515.159',
                                                                   '89.0.1', '90.0.2', '91.0.2', '13.1.2', '14.0.3', '15.0',
                                                                   '91.0.864.59', '92.0.902.78', '93.0.961.52',
                                                                   '76.0.4017.177', '77.0.4054.277', '78.0.4093.147']
        )
        self.__add_provider__(name='locales', elements = ['en_US', 'fr_FR', 'de_DE', 'es_ES', 'zh_CN'])

    def __add_provider__(self, name:str, elements=[]):
        self.faker.add_provider(DynamicProvider(
            provider_name=name,
            elements=elements
        ))

    def __find_generator__(self, col:Column):
        best_match = (-1.0, None)
        for m in dir(self.faker):
            ratio = SequenceMatcher(a=col.name.upper(), b=m.upper()).ratio()
            if ratio > best_match[0]:
                try:
                    best_match = ratio, getattr(self.faker, m)
                except:
                    continue


        return best_match

    def gen(self, col:Column):

        if col.name == "ts":
            if col.type == DataType.STRING:
                return datetime.now().__str__()
            else:
                return round(time.time() * 1000)
        
        dist, method = self.__find_generator__(col=col)
        if dist > .75: # string matches at least 75% of the name
            return method()
        
        match col.type:
            case DataType.INT:
                return random.randint(0, self.limit)
            case DataType.INTEGER:
                return random.randint(0, self.limit)
            case DataType.DOUBLE:
                return random.uniform(0.01, 99.99)
            case DataType.FLOAT:
                return random.uniform(0.01, 99.99)
            case DataType.STRING:
                if col.name in dir(self.faker):
                    return getattr(self.faker,col.name)()
                elif col.name in [m.upper() for m in dir(self.faker)]:
                    return getattr(self.faker,col.name)()
                elif 'COMPANY' in col.name.upper():
                    return self.faker.bs()
                elif 'PHONE' in col.name.upper():
                    return self.faker.phone_number()
                elif 'COMMENT' in col.name.upper() or 'DESCRIPTION' in col.name.upper():
                    return self.faker.paragraph(nb_sentences=3)
                else:
                    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
                
            case DataType.TIMESTAMP:
                return datetime.now().__str__()
            case DataType.DATE:
                return datetime.now().date().__str__()
            case DataType.TIME:
                return datetime.now().time().__str__()
            case DataType.LONG:
                return round(time.time() * 1000)
            case default:
                return "unknown"

    def has_next(self):
        return self.cursor < self.limit
     
    def next(self) -> tuple[str, object]:
        record = {}
        for col_name in self.schema.columns.keys():
            column = self.schema.columns[col_name]
            value = self.gen(column)
            record[col_name] = value

        key = '-'.join([str(self.gen(k)) for k in self.schema.primary_keys.values()])
        try:
            return key, record
        finally:
            self.cursor += 1

class Serializer():
    def JSON(self, key, record:dict):
        data = json.dumps(record)
        return key, data.encode('utf-8')
    
    def AVRO(self, key, record):
        pass


class Sink:
    def __init__(self, gen:Generator, serializer=Serializer().JSON) -> None:
        self.gen = gen
        self.serializer = serializer

    def send(self):
        pass

class StdOut(Sink):
    def __init__(self, gen:Generator) -> None:
        super().__init__(gen=gen)
        
    def send(self):
        while(self.gen.has_next()):
            key, record = self.gen.next()
            data = self.serializer(key, record)
            logger.debug(f'key {key} data {data}')

class CSVFile(Sink):
    def __init__(self, gen: Generator, inputDirURI:str) -> None:
        super().__init__(gen=gen)
        self.input_dir = inputDirURI

    def send(self):

        with open(f'{self.input_dir}/data.csv', 'w') as csvfile:
            records = []
            while(self.gen.has_next()):
                data = self.gen.next()
                field_names = data[1].keys()
                records.append(data[1])

            writer = csv.DictWriter(csvfile, fieldnames = field_names)
            writer.writeheader() 
            writer.writerows(records)


class Kafka(Sink):

    def __init__(self, topic:str, serializer, gen:Generator, bootstrap:str='localhost:9092') -> None:
        super().__init__(serializer=serializer, gen=gen)
        self.topic = topic
        self.bootstrap = bootstrap
        self.p = Producer({'bootstrap.servers': bootstrap})


    def delivery_report(self, err, msg):
        """ Called once for each message produced to indicate delivery result.
            Triggered by poll() or flush(). """
        if err is not None:
            logger.error('Message delivery failed: {}'.format(err))
        else:
            print(f'====> Streaming to Kafka {msg.topic()} [{msg.partition()}]  {clock[random.randint(0,len(clock) - 1)]}            ', end='\r')

    def send(self):
        while(self.gen.has_next()):
            self.p.poll(0)
            key, record = self.gen.next()
            _key, data = self.serializer(key, record)
            self.p.produce(
                key=_key,
                topic=self.topic, 
                value=data, 
                on_delivery=self.delivery_report)
            
            # Wait for any outstanding messages to be delivered and delivery report
            # callbacks to be triggered.
            self.p.flush()
        print(f'Finished stream                                                           ')


app = typer.Typer()
pinot_app = typer.Typer()
pinot_check_app = typer.Typer()
app.add_typer(pinot_app, name="pinot")
pinot_app.add_typer(pinot_check_app, name="check")
kafka_app = typer.Typer()
kafka_check_app = typer.Typer()
app.add_typer(kafka_app, name="kafka")
kafka_app.add_typer(kafka_check_app, name="check")

@pinot_check_app.command()
def table(table:str, host_port='pinot-controller:9000', timeout:int=60):
    """
    Checks and waits for a Pinot table to appear.
    """
    controller(host_port=host_port, timeout=timeout)
    count = 0
    while count < 10:
        api_url = f'http://{host_port}/tables'
        response = requests.get(api_url).json()['tables']
        if table in response:
            print(f'Found Pinot table {table}                                                ')
            return
        else:
            print(f'Waiting for table {table} to appear {clock[count % len(clock)]}', end='\r')
            count+=1
            time.sleep(1)

    raise Exception(f'{table} doesn''t exist')
            
@pinot_check_app.command()
def controller(host_port='pinot-controller:9000', timeout:int=60):
    """
    Checks and waits for the Pinot controller come up
    """
    mustend = int(time.time()) + timeout
    count = 0
    
    while time.time() < mustend:
        try:
            r = requests.get(f'http://{host_port}/tables')
            r.json()
            print(f'Pinot is up 🍷 status {r.status_code}                         ')
            time.sleep(5)
            return True
        except:
            print(f'====> Waiting for 🍷 {clock[count % len(clock)]}            ', end='\r')
            count += 1
            time.sleep(1)

@pinot_app.command()
def batch(schema_path:str, job_spec_yaml:str, stdout:bool=False):
    """
    Generate batch data to a directory
    """
    schema = PinotSchema(schema_path=schema_path)
    job = yaml.load(open(job_spec_yaml), yaml.FullLoader)
    inputDirURI = job['inputDirURI'] # destination directory
    dataFormat = job['recordReaderSpec']['dataFormat'] # where we need to write the data

    if stdout:
        gen = Generator(schema=schema)
        sink = StdOut(gen=gen)
    elif dataFormat.lower() == "csv":
        gen = Generator(schema=schema)
        sink = CSVFile(gen=gen, inputDirURI=inputDirURI)
    else:
        raise Exception(f'{dataFormat} is not supported.')

    sink.send()

@kafka_app.command()
def stream(schema_path:str, config_path:str, stdout:bool=False):
    """
    Generate streaming data to Kafka
    """
    schema = PinotSchema(schema_path=schema_path)
    config = json.load(open(config_path))

    gen = Generator(schema)

    if stdout:
        sink = StdOut(gen=gen)
    else:
        table_type = config['tableType']
        if table_type == "REALTIME":
            stream_config = config['tableIndexConfig']['streamConfigs']
            topic = stream_config['stream.kafka.topic.name']
            if 'stream.kafka.decoder.prop.format' in stream_config:
                format = stream_config['stream.kafka.decoder.prop.format']
            else:
                format = "JSON"
            serializer = Serializer().__getattribute__(format.upper())
            bootstrap = stream_config['stream.kafka.broker.list']
            sink = Kafka(topic=topic, serializer=serializer, gen=gen, bootstrap=bootstrap)
        else:
            raise Exception("table type is not REALTIME")
    sink.send()

@kafka_check_app.command()
def topic(topic:str, bootstrap:str="kafka:9092", timeout=60):
    """
    Checks to see if a Kafka topic exists. TODO
    """
    pass

@kafka_check_app.command()
def broker(bootstrap:str="kafka:9092", timeout:int=60):
    """
    Checks and waits for the Kafka broker to start
    """
    mustend = int(time.time()) + timeout
    count = 0
    while time.time() < mustend:
        try:
            c = socket.socket()
            url = urlparse(f'kafka://{bootstrap}')
            c.connect((url.hostname, url.port))
            print(f'kafka is up {c}                                        ')
            return
        except:
            print(f'Waiting for Kafka {clock[count % len(clock)]}', end='\r')
            time.sleep(1)
            count += 1
        finally:
            c.close()
            
    raise Exception(f'Could not connect to Kafka in {timeout} ms')

if __name__ == "__main__":
    app()