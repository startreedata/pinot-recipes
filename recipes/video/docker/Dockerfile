FROM python:3.11.1

RUN apt-get update -y && \
    apt-get install -y librdkafka-dev

COPY requirements.txt requirements.txt
COPY application.py application.py
COPY batch.py batch.py

RUN pip install --upgrade pip
RUN python3 --version && pip install -r requirements.txt
RUN mkdir out
