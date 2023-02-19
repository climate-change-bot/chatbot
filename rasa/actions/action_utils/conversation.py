def get_last_conversation(events, max_number_of_last_conversations):
    events_cleaned = sorted(events, key=lambda x: x['timestamp'], reverse=True)
    events_cleaned = list(filter(lambda x: x['event'] in ['user', 'bot'], events_cleaned))
    conversation = []
    for event in events_cleaned[0:5]:
        if event['event'] == 'user':
            conversation.append("Benutzer: " + event['text'] + "\n")
        elif event['event'] == 'bot':
            conversation.append("Chatbot: " + event['text'] + "\n")
    return list(reversed(conversation))
