import ctypes
from multiprocessing import Queue, Array, Event, Process
from uuid import uuid4
from random import choice
import glob

from .song import Song


class StreamService:
    def __init__(self, music_library=None):
        self.current_frame = Array(ctypes.c_char, 8192, lock=False)
        self.current_frame_id = Array(ctypes.c_char, len(str(uuid4())),
                                      lock=False)
        self.title = Array('c', 256, lock=False)
        self.artist = Array('c', 256, lock=False)
        self.song_queue = Queue()
        self.next_frame_ready = Event()
        self._p = None

        self.song_pool = []
        self._clients = 0

        self.running = False

        # Parse initial playlist
        if music_library:
            self.song_pool = glob.glob(music_library + '/*.mp3')

    @staticmethod
    def _stream(song_queue, frame_buffer, next_frame_event, title, artist):
        while 1:
            next_song = Song(song_queue.get(), frame_buffer, next_frame_event)
            title.value = ''.join(next_song.title[:255]).encode()
            artist.value = ''.join(next_song.artist[:255]).encode()
            next_song.stream_mp3()

    @staticmethod
    def _monitor_queue(song_queue, song_pool):
        while 1:
            # Add a random song if the queue is empty
            if song_queue.empty():
                song_queue.put(choice(song_pool))

    def skip(self):
        if self.running:
            self.stop_stream()
            self.start_stream()

    def start_stream(self):
        """Start streaming
        """
        print("starting stream processes")
        self._p_2 = Process(target=self._monitor_queue,
                            args=(self.song_queue, self.song_pool))

        self._p_2.start()

        self._p = Process(target=self._stream,
                          args=(self.song_queue, self.current_frame,
                                self.current_frame_id, self.title,
                                self.artist))
        self._p.start()

        self.running = True

    def stop_stream(self):
        """Stop streaming
        """
        print("killing stream processes")
        if self._p:
            self._p.kill()

        if self._p_2:
            self._p_2.kill()

        self.running = True

    def add_song_to_queue(self, song_path):
        self.song_queue.put(song_path)

    def listen(self):
        """Send a stream of live music packets
        """
        print('connect!')
        if self._clients < 1:
            self.start_stream()

        self._clients += 1
        last_frame_sent = None
        while True:
            try:
                if last_frame_sent != self.current_frame_id.raw:
                    last_frame_sent = self.current_frame_id.raw
                    yield self.current_frame.raw

            except GeneratorExit:
                print('disconnect!')
                self._clients -= 1

                print(self._clients)

                if self._clients < 1:
                    self._clients = 0
                    self.stop_stream()

                raise GeneratorExit
