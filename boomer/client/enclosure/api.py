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


from boomer.messagebus.message import Message
from boomer.util.log import getLogger

__author__ = 'jdorleans'

LOGGER = getLogger(__name__)


class EnclosureAPI:
    """
    This API is intended to be used to control Boomer hardware capabilities.

    It exposes all possible enclosure commands to be performed by a Boomer
    unit.
    """

    def __init__(self, client):
        self.client = client

    def system_mute(self):
        self.client.emit(Message("enclosure.system.mute"))

    def system_unmute(self):
        self.client.emit(Message("enclosure.system.unmute"))

    def system_blink(self, times):
        self.client.emit(
            Message("enclosure.system.blink", data={'times': times}))

    def eyes_on(self):
        self.client.emit(Message("enclosure.eyes.on"))

    def eyes_off(self):
        self.client.emit(Message("enclosure.eyes.off"))

    def eyes_blink(self, side):
        self.client.emit(
            Message("enclosure.eyes.blink", data={'side': side}))

    def eyes_narrow(self):
        self.client.emit(Message("enclosure.eyes.narrow"))

    def eyes_look(self, side):
        self.client.emit(
            Message("enclosure.eyes.look", data={'side': side}))

    def eyes_color(self, r=255, g=255, b=255):
        self.client.emit(
            Message("enclosure.eyes.color", data={'r': r, 'g': g, 'b': b}))

    def eyes_brightness(self, level=30):
        self.client.emit(
            Message("enclosure.eyes.level", data={'level': level}))

    def mouth_reset(self):
        self.client.emit(Message("enclosure.mouth.reset"))

    def mouth_talk(self):
        self.client.emit(Message("enclosure.mouth.talk"))

    def mouth_think(self):
        self.client.emit(Message("enclosure.mouth.think"))

    def mouth_listen(self):
        self.client.emit(Message("enclosure.mouth.listen"))

    def mouth_smile(self):
        self.client.emit(Message("enclosure.mouth.smile"))

    def mouth_text(self, text=""):
        self.client.emit(
            Message("enclosure.mouth.text", data={'text': text}))

    def weather_display(self, img_code, temp):
        self.client.emit(
            Message("enclosure.weather.display", data={
                   'img_code': img_code, 'temp': temp}))

    def activate_mouth_listeners(self, active):
        msg = Message('enclosure.mouth.listeners', data={'active': active})
        self.client.emit(msg)
