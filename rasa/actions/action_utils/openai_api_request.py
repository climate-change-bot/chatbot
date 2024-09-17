from openai import OpenAI

from .conversation import get_last_conversation, get_cleaned_chat_gpt_answer

client = OpenAI()

MODEL_INSTRUCTION = "Beantworte die vorherige Nachricht des Users nur, wenn sie mit dem Klimawandel zu tun hat " \
                    "oder wenn die Nachricht im Kontext zu den vorherigen Nachrichten passt. " \
                    "Versuche mit möglichst wenig Worten die Frage zu beantworten. " \
                    "Antworte direkt auf die Frage des users."

FIRST_USER_INSTRUCTION = "Beantworte die vorherige Nachricht des Users nur, wenn sie mit dem Klimawandel zu tun hat " \
                         "oder wenn die Nachricht im Kontext zu den vorherigen Nachrichten passt. " \
                         "Ansonsten antworte das du nur Fragen zum Klimawandel beantwortest. " \
                         "Verwende eine vertraute Anrede (du). " \
                         "Antworte direkt auf die Frage des Users ohne ihn zu begrüssen oder zu erwähnen " \
                         "das die Frage gut ist. "


def request_to_openai(events):
    messages = [{'role': 'system', 'content': MODEL_INSTRUCTION}]
    conversation_items = get_last_conversation(events, 10)
    messages.extend(conversation_items)
    messages.append({'role': 'user', 'content': FIRST_USER_INSTRUCTION})

    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        temperature=0.5
    )
    return completion.choices[0].message.content
