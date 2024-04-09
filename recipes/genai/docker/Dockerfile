FROM python:3.11.1

RUN apt-get update -y && \
    apt-get install -y librdkafka-dev

COPY requirements.txt requirements.txt
COPY loader.py loader.py
COPY genai.py genai.py

RUN pip install --upgrade pip
RUN python3 --version && pip install -r requirements.txt

