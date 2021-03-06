import unittest
import subprocess
import time

from boomer.media.player import FFPlayMediaPlayer


class MockMediaPlayer(FFPlayMediaPlayer):
    """
    MockMediaPlayer
    takes pretend Media, uses the media_type as a way to sneak
    instructions into the mock player (like how long to wait)
    """
    def __init__(self):
        FFPlayMediaPlayer.__init__(self)

    def player_play(self, media):
        sleep_time = media.media_type.get('time_s')
        self.process = \
            subprocess.Popen(['sleep', str(sleep_time)], shell=True,
                             stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        self.process.wait()
        return True


class MediaPlayerTests(unittest.TestCase):
    def setUp(self):
        self.player = MockMediaPlayer()

    def tearDown(self):
        self.player.stop()
        self.player = None

    def testPlayMedia(self):
        events = {}

        def start_event_handler(data):
            events['track_start'] = data

        def end_event_handler(data):
            events['track_end'] = data

        self.player.on('track_start', start_event_handler)
        self.player.on('track_end', end_event_handler)

        self.player.play('test1', {'time_s': 1})
        time.sleep(1)

        self.assertEqual('test1', events.get('track_start').media_uri)
        self.assertEqual('test1', events.get('track_end').media_uri)
