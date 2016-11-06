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

import threading
import time
from Queue import Queue

import pyee
import speech_recognition as sr

from boomer.client.speech.local_recognizer import LocalRecognizer
from boomer.client.speech.mic import MutableMicrophone, ResponsiveRecognizer
from boomer.client.speech.recognizer_wrapper import \
    RemoteRecognizerWrapperFactory
from boomer.configuration import ConfigurationManager
from boomer.messagebus.message import Message
from boomer.metrics import MetricsAggregator
from boomer.session import SessionManager
from boomer.util.log import getLogger

logger = getLogger(__name__)

core_config = ConfigurationManager.get().get('core')
speech_config = ConfigurationManager.get().get('speech_client')
listener_config = ConfigurationManager.get().get('listener')


class AudioProducer(threading.Thread):
    """
    AudioProducer
    given a mic and a recognizer implementation, continuously listens to the
    mic for potential speech chunks and pushes them onto the queue.
    """

    def __init__(self, state, queue, mic, recognizer, emitter):
        threading.Thread.__init__(self)
        self.daemon = True
        self.state = state
        self.queue = queue
        self.mic = mic
        self.recognizer = recognizer
        self.emitter = emitter

    def run(self):
        with self.mic as source:
            self.recognizer.adjust_for_ambient_noise(source)
            while self.state.running:
                try:
                    audio = self.recognizer.listen(source, self.emitter)
                    self.queue.put(audio)
                except IOError, ex:
                    # NOTE: Audio stack on raspi is slightly different, throws
                    # IOError every other listen, almost like it can't handle
                    # buffering audio between listen loops.
                    # The internet was not helpful.
                    # http://stackoverflow.com/questions/10733903/pyaudio-input-overflowed
                    self.emitter.emit("recognizer_loop:ioerror", ex)


class AudioConsumer(threading.Thread):
    """
    AudioConsumer
    Consumes AudioData chunks off the queue
    """

    # In seconds, the minimum audio size to be sent to remote STT
    MIN_AUDIO_SIZE = 0.5

    def __init__(self, state, queue, emitter, wakeup_recognizer,
                 boomer_recognizer, remote_recognizer):
        threading.Thread.__init__(self)
        self.daemon = True
        self.queue = queue
        self.state = state
        self.emitter = emitter
        self.wakeup_recognizer = wakeup_recognizer
        self.boomer_recognizer = boomer_recognizer
        self.remote_recognizer = remote_recognizer
        self.metrics = MetricsAggregator()

    def run(self):
        while self.state.running:
            self.read_audio()

    @staticmethod
    def _audio_length(audio):
        return float(len(audio.frame_data)) / (
            audio.sample_rate * audio.sample_width)

    def read_audio(self):
        audio_data = self.queue.get()

        if self.state.sleeping:
            self.try_wake_up(audio_data)
        else:
            self.process_audio(audio_data)

    def try_wake_up(self, audio):
        if self.wakeup_recognizer.is_recognized(audio.frame_data,
                                                self.metrics):
            SessionManager.touch()
            self.state.sleeping = False
            self.__speak("I'm awake.")  # TODO: Localization
            self.metrics.increment("boomer.wakeup")

    def process_audio(self, audio):
        SessionManager.touch()
        payload = {
            'utterance': self.boomer_recognizer.key_phrase,
            'session': SessionManager.get().session_id,
        }
        self.emitter.emit("recognizer_loop:wakeword", payload)
        try:
            self.transcribe([audio])
        except sr.UnknownValueError:  # TODO: Localization
            logger.warn("Speech Recognition could not understand audio")
            self.__speak("Sorry, I didn't catch that.")

    def __speak(self, utterance):
        payload = {
            'utterance': utterance,
            'session': SessionManager.get().session_id
        }
        self.emitter.emit("speak", Message("speak", metadata=payload))

    def _create_remote_stt_runnable(self, audio, utterances):
        def runnable():
            try:
                text = self.remote_recognizer.transcribe(
                    audio, metrics=self.metrics).lower()
            except sr.UnknownValueError:
                pass
            except sr.RequestError as e:
                logger.error(
                    "Could not request results from Speech Recognition "
                    "service; {0}".format(e))
            except Exception as e:
                logger.error("Unexpected exception: {0}".format(e))
            else:
                logger.debug("STT: " + text)
                if text.strip() != '':
                    utterances.append(text)

        return runnable

    def transcribe(self, audio_segments):
        utterances = []
        threads = []
        logger.debug("Creating remote stt runnable for %d audio segments" % (len(audio_segments)))
        for audio in audio_segments:
            if self._audio_length(audio) < self.MIN_AUDIO_SIZE:
                logger.debug("Audio too short to send to STT")
                continue
            target = self._create_remote_stt_runnable(audio, utterances)
            t = threading.Thread(target=target)
            t.start()
            threads.append(t)
        logger.debug("Created remote stt runable for %d audio segments" % (len(threads)))

        for thread in threads:
            thread.join()
        if len(utterances) > 0:
            payload = {
                'utterances': utterances,
                'session': SessionManager.get().session_id
            }
            self.emitter.emit("recognizer_loop:utterance", payload)
            self.metrics.attr('utterances', utterances)
        else:
            raise sr.UnknownValueError


class RecognizerLoopState(object):
    def __init__(self):
        self.running = False
        self.sleeping = False
        self.skip_wakeword = False


class RecognizerLoop(pyee.EventEmitter):
    def __init__(self, channels=int(speech_config.get('channels')),
                 rate=int(speech_config.get('sample_rate')),
                 device_index=None,
                 lang=core_config.get('lang')):
        pyee.EventEmitter.__init__(self)
        self.microphone = MutableMicrophone(sample_rate=rate,
                                            device_index=device_index)

        # FIXME - channels are not been used
        self.microphone.CHANNELS = channels
        self.boomer_recognizer = self.create_boomer_recognizer(rate, lang)
        # TODO - localization
        self.wakeup_recognizer = self.create_wakeup_recognizer(rate, lang)
        self.remote_recognizer = ResponsiveRecognizer(self.boomer_recognizer)
        self.state = RecognizerLoopState()

    @staticmethod
    def create_boomer_recognizer(rate, lang):
        wake_word = listener_config.get('wake_word')
        phonemes = listener_config.get('phonemes')
        threshold = listener_config.get('threshold')
        return LocalRecognizer(wake_word, phonemes, threshold, rate, lang)

    @staticmethod
    def create_wakeup_recognizer(rate, lang):
        return LocalRecognizer("wake up", "W EY K . AH P", "1e-10", rate, lang)

    def start_async(self):
        self.state.running = True
        queue = Queue()
        AudioProducer(self.state,
                      queue,
                      self.microphone,
                      self.remote_recognizer,
                      self).start()
        AudioConsumer(self.state,
                      queue,
                      self,
                      self.wakeup_recognizer,
                      self.boomer_recognizer,
                      RemoteRecognizerWrapperFactory.wrap_recognizer(
                          self.remote_recognizer)).start()

    def stop(self):
        self.state.running = False

    def mute(self):
        if self.microphone:
            self.microphone.mute()

    def unmute(self):
        if self.microphone:
            self.microphone.unmute()

    def sleep(self):
        self.state.sleeping = True

    def awaken(self):
        self.state.sleeping = False

    def run(self):
        self.start_async()
        while self.state.running:
            try:
                time.sleep(1)
            except KeyboardInterrupt as e:
                logger.error(e)
                self.stop()
