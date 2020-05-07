import ctypes
from multiprocessing import Queue, Array, Event, Process
from random import randint
from io import BytesIO
from uuid import uuid4

from mongoengine import connect

from models.song import Song as SongDB
from .song import Song


class StreamService:
    def __init__(self, **kwargs):
        self.current_frame = Array(ctypes.c_char, 8192, lock=False)
        self.current_frame_id = Array(ctypes.c_char, len(str(uuid4())),
                                      lock=False)
        self.title = Array('c', 256, lock=False)
        self.artist = Array('c', 256, lock=False)
        self.song_queue = Queue()
        self.next_frame_ready = Event()
        self._p = None

        self._mongo_args = kwargs.get('mongo_args', {})

        self._clients = 0

        self.running = False

    @staticmethod
    def _stream(song_queue, frame_buffer, next_frame_event, title, artist,
                mongo_connect_args):
        connect(**mongo_connect_args)
        while 1:
            next_song_db = song_queue.get()
            next_song_bytes = BytesIO(next_song_db.song.read())

            next_song = Song(
                next_song_bytes,
                frame_buffer,
                next_frame_event,
                next_song_db.bitrate
            )

            title.value = ''.join(next_song_db.title[:255]).encode()
            artist.value = ''.join(next_song_db.artist[:255]).encode()

            next_song.stream_mp3()

    @staticmethod
    def _monitor_queue(song_queue, mongo_connect_args):
        connect(**mongo_connect_args)
        while 1:
            # Add a random song if the queue is empty
            if song_queue.empty():
                songs_count = len(SongDB.objects.all())
                song_queue.put(SongDB.objects[randint(0, songs_count-1)])

    def skip(self):
        if self.running:
            self.stop_stream()
            self.start_stream()

    def start_stream(self):
        """Start streaming
        """
        self._p_2 = Process(target=self._monitor_queue,
                            args=(self.song_queue, self._mongo_args))

        self._p_2.start()

        self._p = Process(target=self._stream,
                          args=(self.song_queue, self.current_frame,
                                self.current_frame_id, self.title,
                                self.artist, self._mongo_args))
        self._p.start()

        self.running = True

    def stop_stream(self):
        """Stop streaming
        """
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
