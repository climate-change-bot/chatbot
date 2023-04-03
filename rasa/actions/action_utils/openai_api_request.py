import os
import openai

from .conversation import get_last_conversation, get_cleaned_chat_gpt_answer

openai.api_key = os.getenv("OPENAI_API_KEY")

MODEL_INSTRUCTION = "Beantworte ausschliesslich Fragen die mit dem Klimawandel zu tun haben. " \
                    "Versuche mit möglichst wenig Worten die Frage zu beantworten. " \
                    "Stelle am Schluss deiner Antwort eine Frage die den User in eine Gespräch verwickelt."

FIRST_USER_INSTRUCTION = "Beantworte die nächste Frage des users nur, wenn sie mit dem Klimawandel zu tun hat " \
                         "oder im Kontext der vorherigen Konversation korrekt ist. " \
                         "Ansonsten antworte das du nur Fragen zum Klimawandel beantwortest. " \
                         "Stelle am Schluss deiner Antwort eine Frage, die den User in ein Gespräch verwickelt. " \
                         "Zum Beispiel: wie oft isst du Fleisch? Nutzt du bereits den öffentlich Verkehr? usw." \
                         "Verwende eine vertraute Anrede (du) und eine freundliche Sprache. " \
                         "Vermeide das Wort 'bekämpfen' und antworte ohne Umschweife auf die Frage. "


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
    response_text = get_cleaned_chat_gpt_answer(response["choices"][0]['message']['content'])
    return response_text
