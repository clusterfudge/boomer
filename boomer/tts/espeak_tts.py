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


import subprocess

from boomer.tts import TTS, TTSValidator

__author__ = 'seanfitz'

NAME = 'espeak'


class ESpeak(TTS):
    def __init__(self, lang, voice):
        super(ESpeak, self).__init__(lang, voice)

    def execute(self, sentence):
        voice_parts = []
        if self.lang and len(self.lang.strip()) > 0:
            voice_parts.append(self.lang)
        if self.voice and len(self.voice.strip()) > 0:
            voice_parts.append(self.voice)
        print voice_parts
        subprocess.call(
            ['espeak', '-v', '+'.join(voice_parts), '-s', '140', sentence])


class ESpeakValidator(TTSValidator):
    def __init__(self):
        super(ESpeakValidator, self).__init__()

    def validate_lang(self, lang):
        # TODO
        pass

    def validate_connection(self, tts):
        try:
            subprocess.call(['espeak', '--version'])
        except:
            raise Exception(
                'ESpeak is not installed. Run on terminal: sudo apt-get '
                'install espeak')

    def get_instance(self):
        return ESpeak
