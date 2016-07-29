# Copyright 2016 Boomer AI, Inc.
#
# This file is part of Boomer Core.
#
# Boomer Core is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Boomer Core is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Boomer Core.  If not, see <http://www.gnu.org/licenses/>.


from os.path import dirname, join

from adapt.intent import IntentBuilder
from boomer.skills.core import BoomerSkill

__author__ = 'jasonehines'


# TODO - Localization

class SpeakSkill(BoomerSkill):
    def __init__(self):
        super(SpeakSkill, self).__init__(name="SpeakSkill")

    def initialize(self):
        self.load_vocab_files(join(dirname(__file__), 'vocab', 'en-us'))

        prefixes = [
            'speak', 'say', 'repeat']
        self.__register_prefixed_regex(prefixes, "(?P<Words>.*)")

        intent = IntentBuilder("SpeakIntent").require(
            "SpeakKeyword").require("Words").build()
        self.register_intent(intent, self.handle_speak_intent)

    def __register_prefixed_regex(self, prefixes, suffix_regex):
        for prefix in prefixes:
            self.register_regex(prefix + ' ' + suffix_regex)

    def handle_speak_intent(self, message):
        words = message.metadata.get("Words")
        self.speak(words)

    def stop(self):
        pass


def create_skill():
    return SpeakSkill()
