"""Contains class for describing songs

Authors:
    Chance Nelson <chance-nelson@nau.edu>
"""


from mutagen.mp3 import MP3


class Song:
    def __init__(self, filename):
        """Constructor

        Args:
            filename (string): path to the MP3 file on disk
        """
        metadata = MP3(filename)

        self.song       = str(metadata['TIT2'])
        self.album      = str(metadata['TALB'])
        self.artist     = str(metadata['TPE1'])
        self.mp3_data = None
        with open(filename, 'rb') as fp:
            self.mp3_data = fp.read()

    def getSongChunk(self, size=4096):
        """Read the next chunk of data from the MP3

        Args:
            size (int, optional): number of bytes to read into chunk
        """
        while True:
            chunk = self.mp3_data[:size]
            self.mp3_data = self.mp3_data[size:]
            if not chunk:
                yield None

            else:
                yield chunk

    def __str__(self):
        return '{0} - {1} ({2})'.format(self.artist, self.song, self.album)
