import re

import pandora
from os.path import join, dirname

from adapt.intent import IntentBuilder
from pandora.connection import PandoraConnection

from boomer.media.player import FFPlayMediaPlayer
from boomer.skills.media import MediaSkill
from boomer.util.log import getLogger

log = getLogger("PandoraSkill")

FAILED_AUTH_ERR_MSG = "Could not authenticate to pandora_music for user %s"
EXPIRED_AUTH_MSG = "Exception occurred ensuring pandora_music connection: %s"


class PandoraSkill(MediaSkill):
    def __init__(self):
        super(MediaSkill, self).__init__(name="PandoraSkill")
        self.pandora = None
        self.process = None
        self.station_map = {}
        self.player = FFPlayMediaPlayer()
        self.player.on('track_end', self.handle_next)

    def ensure_connected(self):
        try:
            stations = self.pandora.connection.get_stations(self.pandora.user)
            if not stations or len(stations) == 0:
                raise Exception("Authentication expired, no stations listed.")
        except Exception, e:
            print(EXPIRED_AUTH_MSG % repr(e))
            self.pandora = pandora.Pandora(connection=PandoraConnection())
            authenticated = self.pandora\
                .authenticate(self.config.get('user'), self.config.get('pass'))
            if not authenticated:
                raise Exception(FAILED_AUTH_ERR_MSG % self.config.get('user'))
        return self.pandora

    def initialize(self):
        self.pandora = pandora.Pandora(connection=PandoraConnection())

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

        self.load_data_files(join(dirname(__file__)))

        if not self.config.get('user') or not self.config.get('pass'):
            return

        self.register_stations()
        MediaSkill.initialize(self)

    def register_stations(self):
        station_name_regex = re.compile(r"(.*) Radio")
        p = self.ensure_connected()
        for station in p.stations:
            m = station_name_regex.match(station.get('stationName'))
            if not m:
                continue
            for match in m.groups():
                self.register_vocabulary(match, 'PandoraStation')
                self.station_map[match] = station

    def handle_list_stations(self, message):
        p = self.ensure_connected()
        self.emitter.emit(
            message.reply('pandora:stations', data=p.stations))

    def handle_select_station(self, message):
        p = self.ensure_connected()
        station = self.station_map.get(message.data.get('PandoraStation'))
        try:
            p.switch_station(station)
        except Exception, e:
            print(repr(e))
        next_song = p.get_next_song()
        self.speak_dialog("now.playing.playlist", station)
        self.player.play(
            media_uri=next_song['audioUrlMap']['highQuality']['audioUrl'])

    def handle_pause(self, message):
        self.player.pause()

    def handle_play(self, message):
        self.player.play()

    def handle_next(self, prev_track):
        if self.player.playing:
            p = self.ensure_connected()
            next_song = p.get_next_song()
            self.player.play(
                media_uri=next_song['audioUrlMap']['highQuality']['audioUrl'])

    def stop(self):
        self.player.stop()


def create_skill():
    return PandoraSkill()
