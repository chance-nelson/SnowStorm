import base64
from io import BytesIO

from flask import request, make_response, Blueprint, jsonify
from mongoengine.errors import DoesNotExist
from mutagen.mp3 import MP3

from models.song import Song


LIBRARY = Blueprint('library', __name__, url_prefix='/library')


def _resolve_songs(*songs):
    return [
        {
            'id': i.id,
            'title': i.title,
            'artist': i.artist,
            'runtime': i.runtime,
        }
        for i in songs
    ]


@LIBRARY.route('/', defaults={'song_id': None}, methods=['GET'])
@LIBRARY.route('/<string:song_id>/', methods=['GET'])
def get_songs(song_id: str):
    songs = []
    if song_id:
        try:
            songs.append(Song.objects.get(id=song_id))

        except DoesNotExist:
            return make_response('', 404)

    else:
        songs = Song.objects()

    return make_response(jsonify(_resolve_songs(*songs)), 200)


@LIBRARY.route('/', methods=['PUT'])
def add_song():
    r = request.get_json()

    song_data = base64.b64decode(r.get('song').encode('utf-8'))

    # Read song metadata
    metadata = MP3(BytesIO(song_data))
    title = str(metadata.get('TIT2'))
    album = str(metadata.get('TALB'))
    artist = str(metadata.get('TPE1'))
    runtime = int(metadata.info.length)
    bitrate = int(metadata.info.bitrate)

    new_song = Song(
        title=title,
        artist=artist,
        album=album,
        runtime=runtime,
        bitrate=bitrate,
    )
    new_song.song.put(BytesIO(song_data), content_type='audio/mpeg')
    new_song.save()

    return make_response(jsonify(_resolve_songs(new_song)), 200)
