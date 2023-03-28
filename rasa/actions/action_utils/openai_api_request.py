import os
import openai

from .conversation import get_last_conversation, get_cleaned_chat_gpt_answer

openai.api_key = os.getenv("OPENAI_API_KEY")

MODEL_INSTRUCTION = "Beantworte ausschliesslich Fragen die mit dem Klimawandel zu tun haben."


FIRST_USER_INSTRUCTION = "Beantworte die nächste Frage des users nur, wenn sie mit dem Klimawandel zu tun hat. " \
                         "Ansonsten antworte das du nur Fragen zum Klimawandel beantwortest. " \
                         "Verwende eine vertraute Anrede (du) und eine freundliche Sprache. " \
                         "Vermeide das Wort 'bekämpfen'."


def request_to_openai(events):
    messages = [{'role': 'system', 'content': MODEL_INSTRUCTION}]
    conversation_items = get_last_conversation(events, 7)
    messages.extend(conversation_items)
    messages.insert(-1, {'role': 'user', 'content': FIRST_USER_INSTRUCTION})

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        max_tokens=400,
        temperature=0.7
    )
    response_text = get_cleaned_chat_gpt_answer(response["choices"][0]['message']['content'])
    return response_text
