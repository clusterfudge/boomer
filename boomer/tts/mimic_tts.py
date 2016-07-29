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
#
# Forked from Mycroft Core on 2017-07-29

import subprocess
from os.path import join

from boomer import BOOMER_ROOT_PATH
from boomer.tts import TTS, TTSValidator
from boomer.configuration import ConfigurationManager

__author__ = 'jdorleans'

config = ConfigurationManager.get().get("tts", {})

NAME = 'mimic'
BIN = config.get(
    "mimic.path", join(BOOMER_ROOT_PATH, 'mimic', 'bin', 'mimic'))


class Mimic(TTS):
    def __init__(self, lang, voice):
        super(Mimic, self).__init__(lang, voice)

    def execute(self, sentence):
        subprocess.call([BIN, '-voice', self.voice, '-t', sentence])


class MimicValidator(TTSValidator):
    def __init__(self):
        super(MimicValidator, self).__init__()

    def validate_lang(self, lang):
        pass

    def validate_connection(self, tts):
        try:
            subprocess.call([BIN, '--version'])
        except:
            raise Exception(
                'Mimic is not installed. Make sure install-mimic.sh ran '
                'properly.')

    def get_instance(self):
        return Mimic
