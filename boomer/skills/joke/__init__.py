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

import pyjokes

from adapt.intent import IntentBuilder
from boomer.skills.core import BoomerSkill
from boomer.util.log import getLogger

__author__ = 'crios'

LOGGER = getLogger(__name__)


class JokingSkill(BoomerSkill):
    def __init__(self):
        super(JokingSkill, self).__init__(name="JokingSkill")

    def initialize(self):
        self.load_vocab_files(join(dirname(__file__), 'vocab', self.lang))

        intent = IntentBuilder("JokingIntent").require("JokingKeyword").build()
        self.register_intent(intent, self.handle_intent)

    def handle_intent(self, message):
        self.speak(pyjokes.get_joke(language=self.lang[:-3], category='all'))

    def stop(self):
        pass


def create_skill():
    return JokingSkill()
