import requests


def send_message_rasa(sender_id, message):
    resonse = requests.post('http://localhost:5005/webhooks/rest/webhook',
                            json={"sender": sender_id, "message": message})
    if len(resonse.json()) == 0:
        return "Ich habe dich leider nicht verstanden. Kannst du mir eine andere Frage stellen?"
    return resonse.json()[0]["text"]
