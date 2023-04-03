FROM python:3.10-slim as base

RUN mkdir -p /rasa
WORKDIR /rasa

COPY requirements.txt ./
COPY startup.sh ./
RUN pip3 install -r requirements.txt && \
    python3 -m spacy download de_core_news_md

COPY rasa .

EXPOSE 5005

ENV OPENAI_API_KEY=""

RUN ["chmod", "+x", "startup.sh"]
CMD ./startup.sh