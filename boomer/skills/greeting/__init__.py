import datetime

from adapt.intent import IntentBuilder
from os.path import join, dirname

from boomer.skills.core import BoomerSkill


class GreetingSkill(BoomerSkill):

    TIMES_OF_DAY = [
        (0, "night"),
        (5, "morning"),
        (12, "afternoon"),
        (17, "evening"),
        (20, "night")
    ]

    def __init__(self):
        BoomerSkill.__init__(self, name="GreetingSkill")

    def initialize(self):
        self.load_data_files(join(dirname(__file__)))

        greeting_intent = IntentBuilder('core:greeting')\
            .require('Greeting')\
            .build()

        self.register_intent(greeting_intent, self.handle_greeting)

    def handle_greeting(self, message):
        intent = message.data

        time_of_day = \
            [
                tod for tod in GreetingSkill.TIMES_OF_DAY
                if tod[0] <= datetime.datetime.now().hour
            ][-1][1]

        dialog = "greeting.response.generic"
        if time_of_day == "morning":
            dialog = "greeting.response.morning"
        if time_of_day == "afternoon":
            dialog = "greeting.response.afternoon"
        if time_of_day == "evening":
            dialog = "greeting.response.evening"

        self.speak_dialog(dialog, {})


def create_skill():
    return GreetingSkill()
