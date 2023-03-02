import os
import openai

from .conversation import get_last_conversation

openai.api_key = os.getenv("OPENAI_API_KEY")

MODEL_INSTRUCTION = "Du bist ein freundlicher Chatbot, welcher nur Fragen zum Klimawandel beantwortet."

FIRST_USER_INSTRUCTION = "Beantworte die Frage des user nur, wenn sie mit dem Klimawandel zu tun hat. " \
                         "Ansonsten antworte das du nur Fragen zum Klimawandel beantwortest. " \
                         "Verwende eine vertraute Anrede (du). Freundliche Sprache. Keine Ausrufezeichen. " \
                         "Vermeide das Wort bekämpfen. Grüsse den user nicht."


def request_to_openai(events):
    messages = [{'role': 'system', 'content': MODEL_INSTRUCTION}]
    conversation_items = get_last_conversation(events, 10)
    messages.extend(conversation_items)
    messages.insert(-1, {'role': 'user', 'content': FIRST_USER_INSTRUCTION})

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        max_tokens=400,
        temperature=0.7
    )
    response_text = response["choices"][0]['message']['content']
    return response_text
