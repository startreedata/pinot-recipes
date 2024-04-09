#!/usr/bin/env python3

import json
import sys
from openai import OpenAI
from langchain_community.document_loaders.recursive_url_loader import RecursiveUrlLoader
from bs4 import BeautifulSoup as Soup

from confluent_kafka import Producer

clock = ['>', '=>', '==>', '===>', '====>', '=====>', '======>', '=======>']

class Writer:
    def __init__(self) -> None:
        pass

    def write(self, data:dict): pass

class StdOut(Writer):
    def __init__(self, meta_only=False) -> None:
        super().__init__()
        self.meta_only = meta_only

    def write(self, data:dict):
        print(json.dumps(data['metadata']))
        print(len(data['embedding']))
        if not self.meta_only:
            print(data['embedding'][0:2])


class Kafka(Writer):
    def __init__(self, config:dict) -> None:
        super().__init__()
        self.p = Producer(config)
        self.count = 0

    
    def delivery_report(self, err, msg):
        """ Called once for each message produced to indicate delivery result.
            Triggered by poll() or flush(). """
        if err is not None:
            print('Message delivery failed: {}'.format(err))
        else:
            print(f'====> Streaming to Kafka {msg.topic()} [{msg.partition()}]  {clock[self.count % len(clock)]}            ', end='\r')
            self.count += 1


    def write(self, data: dict):
        self.p.produce(
                key=data['source'],
                topic='documentation', 
                value=json.dumps(data), 
                on_delivery=self.delivery_report)
            
        self.p.flush()

class Loader:
    def __init__(self, url, writer:Writer, model='text-embedding-ada-002') -> None:
        self.url = url
        self.model = model
        self.client = OpenAI()
        self.writer = writer

    def get_embedding(self, text):
        text = text.replace("\n", " ")
        return self.client.embeddings.create(input = [text], model=self.model).data[0]

    def run(self):
        loader = RecursiveUrlLoader(
            url=self.url, use_async=True, max_depth=5, extractor=lambda x: Soup(x, "html.parser").text
        )
        docs = loader.load()

        for doc in docs:
            message = {
                "source": doc.metadata['source'],
                "content": doc.page_content,
                "metadata": doc.metadata,
                "embedding": self.get_embedding(doc.page_content).embedding
            }

            self.writer.write(message)


if __name__ == '__main__':

    args = sys.argv

    writer = Kafka({'bootstrap.servers': 'kafka:9092'})
    # writer = StdOut(meta_only=True)

    l = Loader(url=args[1], writer=writer)
    l.run()
