def send_message_chatgpt(message, bot):
    return bot.send_message(message)['message']
