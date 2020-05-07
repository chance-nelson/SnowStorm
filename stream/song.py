from collections import deque
from datetime import datetime
from time import sleep
from uuid import uuid4

from mutagen.mp3 import MP3


class Song:
    def __init__(self, song_data, stream_buffer, current_frame_id, bitrate):
        self._song_data = song_data
        self._song_chunks = self._load_mp3()
        self._stream_buffer = stream_buffer
        self._current_frame_id = current_frame_id
        self._bitrate = bitrate

    def _load_mp3(self):
        chunks = deque()
        song_raw_chunk = True
        while song_raw_chunk:
            song_raw_chunk = self._song_data.read(8192)
            chunks.append(song_raw_chunk)

        return chunks

    def stream_mp3(self):
        chunk = True

        send_time = 1 / (self._bitrate / (8192 * 8))

        while chunk:
            chunk = self._song_chunks.popleft()

            if not chunk:
                break

            self._stream_buffer.value = chunk
            self._current_frame_id.value = str(uuid4()).encode('utf-8')

            sleep(send_time)
