from typing import Any, Dict, List, Text

from rasa_sdk import Action, Tracker
from rasa_sdk.events import ConversationPaused
from rasa_sdk.executor import CollectingDispatcher

from .action_utils.openai_api_request import request_to_openai


class ActionOpenaiFallback(Action):
    def name(self) -> Text:
        return "action_custom_fallback"

    def run(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        bot_message = request_to_openai(tracker.events)

        dispatcher.utter_message(json_message={"openai": True, "text": bot_message})
        return []
