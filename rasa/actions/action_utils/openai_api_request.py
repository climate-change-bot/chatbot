import os
import openai

from .conversation import get_last_conversation, get_cleaned_chat_gpt_answer

openai.api_key = os.getenv("OPENAI_API_KEY")

MODEL_INSTRUCTION = "Beantworte ausschliesslich Fragen die mit dem Klimawandel zu tun haben. " \
                    "Versuche mit möglichst wenig Worten die Frage zu beantworten. " \
                    "Antworte direkt auf die Frage des users." \
                    "Frage den User am Schluss ob er weitere Fragen zum Klimawandel hat."

FIRST_USER_INSTRUCTION = "Beantworte die vorherige Nachricht des Users nur, wenn sie mit dem Klimawandel zu tun hat " \
                         "oder wenn die Nachricht im Kontext zu den vorherigen Nachrichten passt. " \
                         "Ansonsten antworte das du nur Fragen zum Klimawandel beantwortest. " \
                         "Verwende eine vertraute Anrede (du). " \
                         "Antworte direkt auf die Frage des Users ohne ihn zu begrüssen oder zu erwähnen das die Frage gut ist. "


def request_to_openai(events):
    messages = [{'role': 'system', 'content': MODEL_INSTRUCTION}]
    conversation_items = get_last_conversation(events, 10)
    messages.extend(conversation_items)
    messages.append({'role': 'user', 'content': FIRST_USER_INSTRUCTION})

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        max_tokens=400,
        temperature=0.5
    )
    response_text = get_cleaned_chat_gpt_answer(response["choices"][0]['message']['content'])
    return response_text
