FROM python:3.8-slim as base

RUN mkdir -p /rasa/rasa && \
    mkdir -p /rasa/rasa/models
WORKDIR /rasa

COPY requirements.txt ./
RUN pip3 install -r requirements.txt

COPY rasa .

WORKDIR /rasa/rasa

EXPOSE 5005

CMD [ "rasa", "run", "-vv", "--enable-api", "-endpoints", "endpoints_prod.yml"]