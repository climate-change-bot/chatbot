from bs4 import BeautifulSoup
from markdown import markdown


def _get_cleaned_text(text, is_chatbot_answer):
    html = markdown(text)
    cleaned_text = BeautifulSoup(html, features="html.parser").get_text()
    if is_chatbot_answer:
        cleaned_text = cleaned_text.replace('Herzlich Willkommen :smile:', '')
    return cleaned_text


def _get_text(event):
    if event['text']:
        return event['text']
    return event['data']['custom']['text']


def get_cleaned_chat_gpt_answer(text):
    text = text.replace('!', '.')
    return text


def get_last_conversation(events, max_number_of_last_conversations):
    events_cleaned = sorted(events, key=lambda x: x['timestamp'], reverse=True)
    events_cleaned = list(filter(lambda x: x['event'] in ['user', 'bot'], events_cleaned))
    conversation = []
    for event in events_cleaned[0:max_number_of_last_conversations]:
        if event['event'] == 'user':
            content = _get_cleaned_text(_get_text(event), False)
            if content != '/greet':
                conversation.append({'role': 'user', 'content': content})
        elif event['event'] == 'bot':
            conversation.append({'role': 'assistant', 'content': _get_cleaned_text(_get_text(event), True)})
    return list(reversed(conversation))
