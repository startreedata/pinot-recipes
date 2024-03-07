#!/bin/local/python

import time, string
import random
import json
import os
import logging
import typer
from faker import Faker
import pandas as pd
from confluent_kafka import Producer
from enum import Enum
from datetime import datetime

app = typer.Typer()

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

    def gen(self, col:Column):
        match col.type:
            case DataType.INT:
                return random.randint(0, self.limit)
            case DataType.INTEGER:
                return random.randint()
            case DataType.DOUBLE:
                return random.uniform(0.01, 99.99)
            case DataType.FLOAT:
                return random.uniform(0.01, 99.99)
            case DataType.STRING:
                if 'NAME' in col.name.upper():
                    return self.faker.name()
                elif 'COMPANY' in col.name.upper():
                    return self.faker.bs()
                elif 'ADDRESS' in col.name.upper():
                    return self.faker.address()
                elif 'CITY' in col.name.upper():
                    return self.faker.city()
                elif 'ADDRESS' in col.name.upper():
                    return self.faker.address()
                elif 'PHONE' in col.name.upper():
                    return self.faker.phone_number()
                elif 'COMMENT' in col.name.upper():
                    return self.faker.paragraph(nb_sentences=3)
                elif 'SSN' in col.name.upper():
                    return self.faker.ssn()
                elif 'SBN' in col.name.upper():
                    return self.faker.sbn9()
                else:
                    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
            case DataType.TIMESTAMP:
                return datetime.now().__str__()
            case DataType.DATE:
                return datetime.now().date().__str__()
            case DataType.TIME:
                return datetime.now().time().__str__()
            case default:
                return "unknown"

    def has_next(self):
        return self.cursor < self.limit
     
    def next(self) -> tuple[str, object]:
          self.cursor += 1

class JSONGenerator(Generator):

    def __init__(self, schema:Schema, limit:int=1000):
        super().__init__(schema=schema, limit=limit)
        
    def next(self):
        record = {}
        for col_name in self.schema.columns.keys():
            column = self.schema.columns[col_name]
            value = self.gen(column)
            record[col_name] = value

        key = '-'.join([self.gen(k) for k in self.schema.primary_keys])
            
        data = json.dumps(record)
        try:
            return str(key), data.encode('utf-8')
        finally:
            super().next()
    

class Sink:
    def __init__(self, gen:Generator) -> None:
        self.gen = gen

    def send(self):
        pass

class StdOut(Sink):
    def send(self):
        while(self.gen.has_next()):
            key, data = self.gen.next()
            print(f'key {key} data {data}')  

class Directory(Sink):
    pass

class Kafka(Sink):

    def __init__(self, topic:str, gen:Generator, bootstrap:str='localhost:9092') -> None:
        super().__init__(gen)
        self.topic = topic
        self.bootstrap = bootstrap
        self.p = Producer({'bootstrap.servers': bootstrap})


    def delivery_report(self, err, msg):
        """ Called once for each message produced to indicate delivery result.
            Triggered by poll() or flush(). """
        if err is not None:
            print('Message delivery failed: {}'.format(err))
        else:
            print('Message delivered to {} [{}]'.format(msg.topic(), msg.partition()))


    def send(self):

        while(self.gen.has_next()):
            self.p.poll(0)
            key, data = self.gen.next()
            self.p.produce(
                key=key,
                topic=self.topic, 
                value=data, 
                on_delivery=self.delivery_report)
            
            # Wait for any outstanding messages to be delivered and delivery report
            # callbacks to be triggered.
            self.p.flush()

@app.command()
def produce(schema_path:str, config_path:str, stdout:bool=False):
    """
    Generate data
    """
    schema = PinotSchema(schema_path=schema_path)
    config = json.load(open(config_path))

    gen = JSONGenerator(schema)

    if stdout:
        sink = StdOut(gen=gen)
    else:
        table_type = config['tableType']
        if table_type == "REALTIME":
            stream_config = config['tableIndexConfig']['streamConfigs']
            topic = stream_config['stream.kafka.topic.name']
            bootstrap = stream_config['stream.kafka.broker.list']
            sink = Kafka(topic=topic, gen=gen, bootstrap=bootstrap)
        else:
            sink = Directory()
    
    sink.send()

if __name__ == "__main__":
    app()