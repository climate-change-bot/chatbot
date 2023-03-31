from typing import List

from ftlangdetect import detect

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
            if isinstance(user_text, str) and user_text != '/greet' and len(user_text.strip()) > 15:
                try:
                    detected_language = detect(user_text)
                except:
                    detected_language = {'lang': 'unknown'}

                if detected_language['lang'] != 'de' or (
                        detected_language['lang'] == 'de' and detected_language['score'] < 0.5):
                    message.set("intent", {"name": "language_error", "confidence": 1.0}, add_to_output=True)
        return messages
