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


import configparser
import random
import time
import sys

from icecast import Icecast
from song import Song
from songqueue import SongQueue


config_file = None

try:
    config_file = sys.argv[1]

except:
    config_file = 'config.ini'
    #print("Usage: {0} <config file path>".format(sys.argv[0]))
    #exit()

config = configparser.ConfigParser()
config.read(config_file)

host       = str(config['SERVER']['host'])
port       = int(config['SERVER']['port'])
source_pwd = str(config['SERVER']['source_password'])
mount      = str(config['SERVER']['mount'])
admin_pwd  = str(config['SERVER']['admin_password'])

playlist = str(config['MUSIC']['playlist'])


# Parse the playlist file and grab all availabel songs
songs = []
with open(playlist, 'r') as fp:
    songs = fp.read().split('\n')

# Remove any empty strings
songs = list(filter(None, songs))

song_queue = SongQueue()

#random.shuffle(songs)

# Populate the song queue with the available songs
#for song in songs:
#    song_queue.add(Song(song))

radio = Icecast(host, port, source_pwd, mount, song_queue, admin_password=admin_pwd)

radio.stream()

while True:
    time.sleep(1)
