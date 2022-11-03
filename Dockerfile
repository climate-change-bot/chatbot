FROM python:3.8-slim as base

RUN mkdir -p /rasa
WORKDIR /rasa

COPY requirements.txt ./
RUN pip3 install -r requirements.txt

COPY rasa .

EXPOSE 5005

CMD ["rasa", "run", "--enable-api", "--endpoints", "endpointsProd.yml"]