import signal
import subprocess
import os
import threading
import pyee

__author__ = "seanfitz"


class Media(object):
    def __init__(self, media_uri, media_type):
        self.media_uri = media_uri
        self.media_type = media_type


class MediaPlayer(pyee.EventEmitter):
    def __init__(self):
        pyee.EventEmitter.__init__(self)
        self.playlist = []
        self.playlist_position = 0
        self.loop = False
        self.playing = False
        self.paused = False

    def stop(self):
        self.clear_playlist()
        self.playing = False
        self.paused = False
        self.player_stop()

    def play(self, media_uri=None, media_type=None):
        if media_uri:
            if self.playing:
                self.player_stop()
            self.clear_playlist()
            self.queue_media(media_uri, media_type)
            self.start_playlist()
        elif self.playing and self.paused:
            self.player_resume()
        elif not self.playing:
            self.paused = False
            self.playing = True
            self.start_playlist()

    def start_playlist(self):

        def target(player):
            while player.playing \
                    and player.playlist_position < len(player.playlist):
                media = player.playlist[player.playlist_position]
                player.emit('track_start', media)
                should_signal = player.player_play(media)
                if should_signal:
                    player.emit('track_end', media)
                player.playlist_position += 1
                if player.playlist_position == len(player.playlist) \
                        and player.loop:
                    player.playlist_position = 0
            player.playing = False

        self.playing = True
        self.paused = False
        thread = threading.Thread(target=target, args=(self,))
        thread.daemon = False
        thread.start()

    def pause(self):
        if self.playing and not self.paused:
            self.player_pause()
            self.paused = True
        elif self.playing and self.paused:
            self.player_resume()
            self.paused = False

    def queue_media(self, media_uri, media_type=None):
        self.playlist.append(Media(media_uri, media_type))

    def clear_playlist(self):
        self.playlist = []
        self.playlist_position = 0

    def loop(self):
        self.loop = not self.loop

    def shuffle(self):
        pass

    def player_play(self, media):
        raise NotImplementedError()

    def player_resume(self):
        raise NotImplementedError()

    def player_pause(self):
        raise NotImplementedError()

    def player_stop(self):
        raise NotImplementedError()


class FFPlayMediaPlayer(MediaPlayer):
    def __init__(self):
        MediaPlayer.__init__(self)
        self.process = None
        self.should_signal = True

    def player_play(self, media):
        self.should_signal = True
        try:
            self.process = \
                subprocess.Popen(['ffplay', '-nodisp', '-autoexit', media.media_uri],
                                 stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                 stdin=subprocess.PIPE)
            self.process.communicate()
            return self.should_signal
        except OSError, e:
            if e.errno == signal.SIGTERM:
                self.should_signal = False

            return self.should_signal

        finally:
            self.process = None
            self.should_signal = True

    def player_resume(self):
        if self.process:
            os.kill(self.process.pid, signal.SIGCONT)

    def player_stop(self):
        if self.process:
            self.should_signal = False
            try:
                os.kill(self.process.pid, signal.SIGKILL)
            except OSError, e:
                if e.errno != 3: # no such pid
                    raise e

    def player_pause(self):
        if self.process:
            os.kill(self.process.pid, signal.SIGSTOP)
