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

import sys
from threading import Thread, Lock

from boomer.messagebus.client.ws import WebsocketClient
from boomer.messagebus.message import Message
from boomer.tts import tts_factory
from boomer.util.log import getLogger

tts = tts_factory.create()
client = None
mutex = Lock()
logger = getLogger("CLIClient")


def handle_speak(event):
    mutex.acquire()
    client.emit(Message("recognizer_loop:audio_output_start"))
    try:
        utterance = event.data.get('utterance')
        logger.info("Speak: " + utterance)
        tts.execute(utterance)
    finally:
        mutex.release()
        client.emit(Message("recognizer_loop:audio_output_end"))


def connect():
    client.run_forever()


def main():
    global client
    client = WebsocketClient()
    if '--quiet' not in sys.argv:
        client.on('speak', handle_speak)
    event_thread = Thread(target=connect)
    event_thread.setDaemon(True)
    event_thread.start()
    try:
        while True:
            print("Input:")
            line = sys.stdin.readline()
            client.emit(
                Message("recognizer_loop:utterance",
                        data={'utterances': [line.strip()]}))
    except KeyboardInterrupt, e:
        logger.exception(e)
        event_thread.exit()
        sys.exit()


if __name__ == "__main__":
    main()
