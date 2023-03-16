from typing import Text, List

from rasa_sdk.executor import CollectingDispatcher, Tracker
from rasa_sdk.forms import FormValidationAction
from rasa_sdk.types import DomainDict


class ValidateQuizForm(FormValidationAction):
    _last_send_template = {}

    def name(self) -> Text:
        return "validate_quiz_form"

    def _get_last_send_template(self, user_id):
        if user_id in self._last_send_template:
            return self._last_send_template[user_id]
        self._last_send_template[user_id] = ""
        return ""

    @staticmethod
    def _get_last_bot_utter_action(events):
        for event in list(reversed(events)):
            if event['event'] == 'bot' and 'utter_action' in event['metadata']:
                return event['metadata']['utter_action']

    @staticmethod
    def _is_last_question(domain_slots, slot_values):
        for domain_slot in domain_slots:
            if slot_values[domain_slot] is None:
                return False
        return True

    @staticmethod
    def _number_of_correct_answers(domain_slots, slot_values):
        correct_answers = 0
        for domain_slot in domain_slots:
            if slot_values[domain_slot].startswith('true_'):
                correct_answers += 1
        return correct_answers

    async def required_slots(
            self,
            domain_slots: List[Text],
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict,
    ) -> List[Text]:
        if tracker.slots['requested_slot']:
            current_slot = tracker.slots['requested_slot']
            current_slot_entity = tracker.slots[current_slot]
            next_utter = f"utter_quiz_{current_slot}_{current_slot_entity}"
            last_utter_action = self._get_last_send_template(tracker.sender_id)
            last_utter_bot_action = self._get_last_bot_utter_action(tracker.events)
            # This hack is needed because rasa has a bug and calls the method multiple times
            if next_utter != last_utter_action and next_utter != last_utter_bot_action:
                self._last_send_template[tracker.sender_id] = next_utter
                dispatcher.utter_message(response=next_utter)
                if self._is_last_question(domain_slots, tracker.slots):
                    number = self._number_of_correct_answers(domain_slots, tracker.slots)
                    dispatcher.utter_message(text=f"Du hast {number} richtige Antworten")

        return domain_slots
