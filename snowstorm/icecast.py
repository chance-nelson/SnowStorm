"""Contains class for handling connections and streaming to the Icecast server

Authors:
    Chance Nelson <chance-nelson@nau.edu>

"""

import logging
from multiprocessing import Process, Queue, Event

from shouty.connection import Connection
import shouty.enums

import requests
from requests.auth import HTTPBasicAuth


class Icecast:
    def __init__(self, host, port, source_password, mount, queue, 
                 admin_password=None):
        """Constructor

        Args:
            host (string): Icecast server host
            port (int): Icecast server port
            source_password (string): Password to open Icecast source
            mount (string): Mount point to open source at
            next_chunk (function): Function that will give the next chunk of
                data to send to the Icecast server
            admin_password (string, optional): Password to the Icecast admin
                interface. This is only needed if you wish to update metadata
                through the admin API.
        """
        self.__params = {
            'host': host,
            'port': port,
            'user': 'source',
            'password': source_password,
            'format': shouty.Format.MP3,
            'mount': mount
        }

        self.__stream_thread  = None
        self.__stop_streaming = Event()
        self.__queue = queue;
        self.__current_song = None;

        self.__admin_password = admin_password
        self.cnx = Connection(**self.__params)
        self.cnx.open()

    def updateMetadata(self, song_name, artist=None):
        """Update stream metadata.

        If the admin_password flag was set during instantiation, metadata
        will be updated via Icecast's available admin interface web API.
        Otherwise, metadata will be prepared via shouty and sent as part of
        the stream.

        Args:
            song_name (string): song name
            artist (string, optional): artist name
        """
        song_name = ''
        if artist:
            song_name = '{0} - '.format(artist)

        song_name += '{0}'.format(song_name)

        if self.__admin_password:
            url_args = {}
            url_args['song'] = song_name
            url_args['mode'] = 'updinfo'
            url_args['mount'] = self.__params['mount']

            url = 'http://{0}:{1}'.format(self.__params['host'], 
                                          self.__params['port'])
            url += '/admin/metadata'

           
            requests.get(url, params=url_args, 
                         auth=HTTPBasicAuth('admin', self.__admin_password))

        else:
            meta = self.cnx.set_metadata_song(song_name)

    def stream(self):
        """Stream to the Icecast server

        Opens a thread, and will continue to pull from self.__next_chunk()
        and send that file data. This thread is killed when closeConnection()
        is called, or the object is deleted.
        """
        self.__stream_thread = Process(target=self.__streamData)
        self.__stream_thread.start()

    def __streamData(self):
        """Stream data chunks to the Icecast server
        """
        while not self.__stop_streaming.is_set():
            if not self.__current_song:
                try:
                    self.__current_song = self.__queue.pop()
                    print('moving to next song')

                except:
                    print('no next song found')
                    self.cnx.send(bytes(4096))
                    self.cnx.sync()
                    continue
            
            for chunk in self.__current_song.getSongChunk():
                if not chunk:
                    self.current_song = None
                    self.cnx.send(bytes(4096))
                    self.__current_song = None
                    self.cnx.sync()
                    break

                else:
                    self.cnx.send(chunk)
                    self.cnx.sync()
   
    def __del__(self):
        """Terminate the connection to Icecast
        """
        if self.__stream_thread:
            self.__stop_streaming.set()
            
            while self.__stream_thread.is_alive():
                pass

        self.cnx.close()
        self.cnx.free()
