from bs4 import BeautifulSoup
from markdown import markdown


def _get_cleaned_text(text):
    html = markdown(text)
    return ' '.join(BeautifulSoup(html).findAll(text=True))


def get_last_conversation(events, max_number_of_last_conversations):
    events_cleaned = sorted(events, key=lambda x: x['timestamp'], reverse=True)
    events_cleaned = list(filter(lambda x: x['event'] in ['user', 'bot'], events_cleaned))
    conversation = []
    for event in events_cleaned[0:max_number_of_last_conversations]:
        if event['event'] == 'user':
            conversation.append("Benutzer: " + _get_cleaned_text(event['text']) + "\n")
        elif event['event'] == 'bot':
            conversation.append("Chatbot: " + _get_cleaned_text(event['text']) + "\n")
    return list(reversed(conversation))
