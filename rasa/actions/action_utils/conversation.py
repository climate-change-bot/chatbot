from bs4 import BeautifulSoup
from markdown import markdown


def _get_cleaned_text(text):
    html = markdown(text)
    return BeautifulSoup(html, features="html.parser").get_text()


def _get_text(event):
    if event['text']:
        return event['text']
    return event['data']['custom']['text']


def _filter_quiz_events(events):
    events_without_quiz = []
    is_quiz = False
    for event in events:
        if event['event'] == 'user' and event['parse_data']['intent']['name'] == 'start_quiz':
            is_quiz = True
        elif 'name' in event and event['name'] == 'action_reset_slots':
            is_quiz = False

        if not is_quiz:
            events_without_quiz.append(event)
    return events_without_quiz


def get_last_conversation(events, max_number_of_last_conversations):
    events = _filter_quiz_events(events)
    events_cleaned = sorted(events, key=lambda x: x['timestamp'], reverse=True)
    events_cleaned = list(filter(lambda x: x['event'] in ['user', 'bot'], events_cleaned))
    conversation = []
    for event in events_cleaned[0:max_number_of_last_conversations]:
        if event['event'] == 'user':
            content = _get_cleaned_text(_get_text(event))
            if content != '/greet':
                conversation.append({'role': 'user', 'content': content})
        elif event['event'] == 'bot':
            conversation.append({'role': 'assistant', 'content': _get_cleaned_text(_get_text(event))})
    return list(reversed(conversation))
