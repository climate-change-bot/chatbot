FROM python:3.8-slim as base

RUN mkdir -p /rasa
WORKDIR /rasa

COPY requirements.txt ./
RUN pip3 install -r requirements.txt && \
    python3 -m spacy download de_core_news_md

COPY rasa .

EXPOSE 5005

CMD ["rasa", "run", "--enable-api", "--endpoints", "endpointsProd.yml"]