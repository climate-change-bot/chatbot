# RASA/ChatGPT Chatbot Component for Climate Change Bot

[![ci](https://github.com/climate-change-bot/chatbot/actions/workflows/ci.yml/badge.svg)](https://github.com/climate-change-bot/chatbot/actions/workflows/ci.yml)

This is the chatbot component of the Climate Change Bot project. The goal of this project is to develop a chatbot that
can answer questions about climate change.

## Restrictions

- The chatbot is currently only optimized for german
- The chatbot is only accessible from [www.climate-change-bot.site](https://www.climate-change-bot.site).

## Code Entry Points

- All Intents, Rules and Stories are defined in [rasa/data](rasa/data)
- Configuration of the rasa pipeline [rasa/config.yml](rasa/config.yml)
- Responses and definition of slots [rasa/domain](rasa/domain)
- Code of the rasa action server [rasa/actions](rasa/actions)

## Running the Code

Only described for linux. 

- Install first python 3.10.
- Create a virtual environment and install the packages in the requirements.txt.
- Comment out the tracker_store section to use the InMemoryTrackerStore. Otherwise, you  need to install the postgres database and set the correct settings.
- Navigate in the console to the rasa folder.
- Build the rasa model.
```bash 
rasa train --domain domain
```
- Run the chatbot.
```bash 
rasa run -vv --enable-api -m ./models/ --endpoints endpoints.yml
```
- Open another console to run the action server and navigate to the rasa folder.
- Set the environment variable with your OpenAI ChatGPT API Key and run the action server.
```bash 
export OPENAI_API_KEY=your_key

rasa run actions --actions actions --port 5055
```