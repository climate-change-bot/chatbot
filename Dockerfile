FROM python:3.8-slim as base

RUN mkdir -p /rasa
WORKDIR /rasa

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential \
        gcc \
        g++ && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./
COPY startup.sh ./
RUN pip3 install -r requirements.txt && \
    python3 -m spacy download de_core_news_md

COPY rasa .

EXPOSE 5005

ENV OPENAI_API_KEY=""

RUN ["chmod", "+x", "startup.sh"]
CMD ./startup.sh