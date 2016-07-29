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

from gtts import gTTS

from boomer.tts import TTS, TTSValidator
from boomer.util import play_wav

__author__ = 'jdorleans'

NAME = 'gtts'


class GoogleTTS(TTS):
    def __init__(self, lang, voice):
        super(GoogleTTS, self).__init__(lang, voice)

    def execute(self, sentence):
        tts = gTTS(text=sentence, lang=self.lang)
        tts.save(self.filename)
        play_wav(self.filename)


class GoogleTTSValidator(TTSValidator):
    def __init__(self):
        super(GoogleTTSValidator, self).__init__()

    def validate_lang(self, lang):
        # TODO
        pass

    def validate_connection(self, tts):
        try:
            gTTS(text='Hi').save(tts.filename)
        except:
            raise Exception(
                'GoogleTTS server could not be verified. Please check your '
                'internet connection.')

    def get_instance(self):
        return GoogleTTS
