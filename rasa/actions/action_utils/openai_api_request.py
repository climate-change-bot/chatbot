import os
import openai

from .conversation import get_last_conversation
from .response import clean_response

openai.api_key = os.getenv("OPENAI_API_KEY")

BASE_REQUEST = "Nächste Antwort wenn sich die letzte Antwort des Benutzer auf den Klimawandel bezieht. Andernfalls " \
               "beantworte die Fragen nicht und antworte, dass nur Fragen zum Klimawandel beantwortet werden. " \
               "Verwende generell eine vertraute Anrede (du), freundliche Sprache und keine Ausrufezeichen. " \
               "Verwende nicht das Wort bekämpfen.\n"


def request_to_openai(events):
    conversation_items = get_last_conversation(events, 5)
    text = BASE_REQUEST
    for conversation in conversation_items:
        text += conversation

    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=text,
        max_tokens=400,
        temperature=0.7
    )
    response_text = clean_response(response["choices"][0].text)
    return response_text


if __name__ == "__main__":
    request_to_openai('1')
