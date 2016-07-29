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

from boomer.configuration import ConfigurationManager
from boomer.util.log import getLogger

__author__ = 'seanfitz'

log = getLogger("RecognizerWrapper")

config = ConfigurationManager.get().get('speech_client')


class GoogleRecognizerWrapper(object):
    def __init__(self, recognizer):
        self.recognizer = recognizer

    def transcribe(
            self, audio, language="en-US", show_all=False, metrics=None):
        key = config.get('goog_api_key')
        return self.recognizer.recognize_google(
            audio, key=key, language=language, show_all=show_all)


class WitRecognizerWrapper(object):
    def __init__(self, recognizer):
        self.recognizer = recognizer

    def transcribe(
            self, audio, language="en-US", show_all=False, metrics=None):
        assert language == "en-US", \
            "language must be default, language parameter not supported."
        key = config.get('wit_api_key')
        return self.recognizer.recognize_wit(audio, key, show_all=show_all)


class IBMRecognizerWrapper(object):
    def __init__(self, recognizer):
        self.recognizer = recognizer

    def transcribe(
            self, audio, language="en-US", show_all=False, metrics=None):
        username = config.get('ibm_username')
        password = config.get('ibm_password')
        return self.recognizer.recognize_ibm(
            audio, username, password, language=language, show_all=show_all)


RECOGNIZER_IMPLS = {
    'google': GoogleRecognizerWrapper,
    'wit': WitRecognizerWrapper,
    'ibm': IBMRecognizerWrapper
}


class RemoteRecognizerWrapperFactory(object):
    @staticmethod
    def wrap_recognizer(recognizer, impl=config.get('recognizer_impl')):
        if impl not in RECOGNIZER_IMPLS.keys():
            raise NotImplementedError("%s recognizer not implemented." % impl)

        impl_class = RECOGNIZER_IMPLS.get(impl)
        return impl_class(recognizer)
