#!/usr/bin/env python


"""Main file for the Radio

The radio primarily works by opening a persistent connection with the use of
the shouty library. If an admin password is supplied, streaming a new song
will also result in the accessing of the admin interface and updating the
metadata for the stream endpoint.

__main__ currently creates a new mount point based on arguments in a config
file that is supplied by the user, and shuffle-repeating endlessly through
a supplied .m3u playlist file.

"""


from shouty.connection import Connection
import shouty.enums
import requests
from requests.auth import HTTPBasicAuth
from mutagen.mp3 import MP3
import configparser
import random
import sys
import threading


class SnowStorm:
    def __init__(self, host, port, source_password, mount, admin_password=None):
        self.__params = {
            'host': host,
            'port': port,
            'user': 'source',
            'password': source_password,
            'format': shouty.Format.MP3,
            'mount': mount
        }

        self.__admin_password = admin_password
        self.cnx = Connection(**self.__params)
        self.cnx.open()


    def updateMetadata(self, filename):
        """Update the Icecast metadata based on song file information.

        Args:
            filename (str): file path to the MP3
        """
        # Open the file in mutagen and get the metadata
        metadata = MP3(filename)

        song = metadata

        song   = str(metadata['TIT2'])
        album  = str(metadata['TALB'])
        artist = str(metadata['TPE1'])

        url_args = {
            'song': song,
            'ualbum': album,
            'artist': artist,
            'mode': 'updinfo',
            'mount': self.__params['mount']
        }

        url = 'http://{0}:{1}'.format(self.__params['host'], 
                                      self.__params['port'])
        url += '/admin/metadata'

       
        requests.get(url, params=url_args, 
                     auth=HTTPBasicAuth('admin', self.__admin_password))


    def streamFile(self, filename):
        """Stream a file to the Icecast server

        Args:
            filename (str): file path to the MP3
        """
        if self.__admin_password:
            self.updateMetadata(filename)

        self.cnx.send_file(filename)

    
    def closeConnection(self):
        """Terminate the connection to Icecast
        """
        self.cnx.close()
        self.cnx.free()


if __name__ == '__main__':
    config_file = None
    
    try:
        config_file = sys.argv[1]

    except:
        print("Usage: {0} <config file path>".format(sys.argv[0]))
        exit()

    config = configparser.ConfigParser()
    config.read(config_file)

    host       = str(config['SERVER']['host'])
    port       = int(config['SERVER']['port'])
    source_pwd = str(config['SERVER']['source_password'])
    mount      = str(config['SERVER']['mount'])
    admin_pwd  = str(config['SERVER']['admin_password'])

    playlist = str(config['MUSIC']['playlist'])

    radio = SnowStorm(host, port, source_pwd, mount, admin_pwd)

    # Parse the playlist file and grab all availabel songs
    songs = []
    with open(playlist, 'r') as fp:
        songs = fp.read().split('\n')

    # Remove any empty strings
    songs = list(filter(None, songs))

    while True:
        random.shuffle(songs)

        for song in songs:
            radio.streamFile(song)
