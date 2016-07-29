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


import feedparser
import time
from os.path import dirname

import boomer.skills.weather as weather
from adapt.intent import IntentBuilder
from boomer.skills.core import BoomerSkill
from boomer.util import play_mp3
from boomer.util.log import getLogger

__author__ = 'jdorleans'

LOGGER = getLogger(__name__)


class NPRNewsSkill(BoomerSkill):
    def __init__(self):
        super(NPRNewsSkill, self).__init__(name="NPRNewsSkill")
        self.url_rss = self.config['url_rss']
        self.weather = weather.WeatherSkill()
        self.process = None

    def initialize(self):
        self.load_data_files(dirname(__file__))
        intent = IntentBuilder("NPRNewsIntent").require(
            "NPRNewsKeyword").build()
        self.register_intent(intent, self.handle_intent)

        self.weather.bind(self.emitter)
        self.weather.load_data_files(dirname(weather.__file__))

    def handle_intent(self, message):
        try:
            data = feedparser.parse(self.url_rss)
            self.speak_dialog('npr.news')
            time.sleep(3)
            self.process = play_mp3(data['entries'][0]['links'][0]['href'])

        except Exception as e:
            LOGGER.error("Error: {0}".format(e))

    def stop(self):
        if self.process and self.process.poll() is None:
            self.speak_dialog('npr.news.stop')
            self.process.terminate()
            self.process.wait()


def create_skill():
    return NPRNewsSkill()
