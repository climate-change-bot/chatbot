import re


def clean_response(text):
    text = text.strip()
    return re.sub(r"^[Cc]hatbot:", "", text).strip()
