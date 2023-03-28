from abc import ABC
from typing import List

from langdetect import detect

from rasa.engine.graph import GraphComponent
from rasa.engine.recipes.default_recipe import DefaultV1Recipe
from rasa.nlu.classifiers.classifier import IntentClassifier
from rasa.shared.nlu.training_data.message import Message


@DefaultV1Recipe.register(
    DefaultV1Recipe.ComponentType.INTENT_CLASSIFIER, is_trainable=False
)
class LanguageFilter(GraphComponent, IntentClassifier):

    def process(self, messages: List[Message]) -> List[Message]:
        if len(messages) > 0:
            message = messages[0]
            user_text = message.data['text']
            if user_text != '/greet' and len(user_text) > 10:
                try:
                    detected_language = detect(user_text)
                except:
                    detected_language = "unknown"

                if detected_language != "de":
                    message.set("intent", {"name": "language_error", "confidence": 1.0}, add_to_output=True)
        return messages
