from pyChatGPT import ChatGPT
import time
from rasa_client import send_message_rasa
from chatgpt_client import send_message_chatgpt
import uuid
import os

initial_chat_gpt_command = "Simuliere in dieser Konversation nur den Nutzer eines Chatbots, " \
                           "welcher sich mit dem Chatbot über den Klimawandel unterhält. " \
                           "Meine Antworten auf deinen Text sind " \
                           "dabei die Antworten des Chatbots. Die Fragen des Users sollen so kurz wie möglich sein. " \
                           "Die erste Meldung des Chatbots ist folgende:\n"

following_chat_gpt_command = "Reagiere nun als simulierter Benutzer auf die folgende Nachricht des Chatbots:\n"


def start_simulation_of_user():
    number_of_conversations = 5
    for i in range(number_of_conversations):
        simulation_of_one_conversation()


def simulation_of_one_conversation():
    sender_id = f"chatgpt-{str(uuid.uuid4())}"
    rasa_bot_message = send_message_rasa(sender_id, "/greet")
    print(f"Chatbot: {rasa_bot_message}")
    bot = ChatGPT(os.environ["SESSION_TOKEN"])
    chat_gpt_command = initial_chat_gpt_command + rasa_bot_message
    number_of_turns = 15
    for i in range(number_of_turns):
        chat_gpt_response = send_message_chatgpt(chat_gpt_command, bot)
        rasa_bot_message = send_message_rasa(sender_id, chat_gpt_response)
        print(f"User: {chat_gpt_response}")
        print(f"Chatbot: {rasa_bot_message}")
        chat_gpt_command = following_chat_gpt_command + rasa_bot_message
        time.sleep(10)


if __name__ == '__main__':
    start_simulation_of_user()
