import re

import pandora
from adapt.intent import IntentBuilder
from pandora.connection import PandoraConnection

from boomer.skills.media import MediaSkill


class PandoraSkill(MediaSkill):
    def __init__(self):
        super(MediaSkill, self).__init__(name="PandoraSkill")
        self.pandora = None
        self.process = None
        self.station_map = {}

    def ensure_connected(self):
        try:
            stations = self.pandora.connection.get_stations(self.pandora.user)
            if len(stations) == 0:
                raise Exception("Authentication expired, no stations listed.")
        except Exception, e:
            print("Exception occurred ensuring pandora_music connection: %s" % repr(e))
            self.pandora = pandora.Pandora(connection=PandoraConnection())
            if not self.pandora.authenticate(self.config.get('user'), self.config.get('pass')):
                raise Exception("Could not authenticate to pandora_music for user %s" % self.pandora_config.get('user'))
        return self.pandora

    def initialize(self):
        self.pandora = pandora.Pandora(connection=pandora.connection.PandoraConnection())

        # setup intents
        list_stations_intent = IntentBuilder('pandoralist_stations')\
            .require('BrowseMusicCommand')\
            .build()

        self.register_intent(list_stations_intent, self.handle_list_stations)

        play_music_command = IntentBuilder('pandora:select_station') \
            .require('ListenCommand') \
            .require('PandoraStation') \
            .optionally('MusicKeyword') \
            .build()
        self.register_intent(play_music_command, self.handle_select_station)

        self.register_stations()

    def register_stations(self):
        station_name_regex = re.compile(r"(.*) Radio")
        p = self.ensure_connected()
        for station in p.stations:
            m = station_name_regex.match(station.get('stationName'))
            if not m:
                continue
            for match in m.groups():
                self.register_vocabulary(match, 'PandoraStation')
                self.station_map[match] = station.get('stationId')

    def handle_list_stations(self, messsage):
        p = self.ensure_connected()
        station = [s for s in self.pandora.stations if s.get('stationName')][0]
        pass

    def handle_select_station(self, message):
        pass


def create_skill():
    return PandoraSkill()
