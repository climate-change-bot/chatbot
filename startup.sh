#!/bin/sh

rasa run --enable-api --endpoints endpointsProd.yml &
rasa run actions --actions actions --port 5055