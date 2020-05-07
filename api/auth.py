from flask import Response, request, current_app, make_response, Blueprint
import jwt
from mongoengine.errors import DoesNotExist
from mutagen.mp3 import MP3

from .models import Song


AUTH = Blueprint('stream', __name__, url_prefix='/library')


@AUTH.route('/skip')
def skip():
    current_app.config.get('stream').skip()
    return make_response('', 200)


@AUTH.route('/stream.mp3')
def stream():
    return Response(current_app.config.get('stream').listen(),
                    mimetype='audio/mpeg')


@AUTH.route(
    '/<string:song_id>',
    methods=['GET'],
    defaults={'song_id': None}
)
def get_songs(song_id: str):
    songs = []
    if song_id:
        try:
            songs.append(Song.objects.get(id=song_id))

        except DoesNotExist:
            return make_response('', 404)

    else:
        songs = Song.objects()

    return make_response(
        [
            {
                'id': i.id,
                'name': i.name,
                'artist': i.artist,
                'runtime': i.runtime,
            }
            for i in songs
        ],
        200
    )


@AUTH.route('/', methods=['PUT'])
def add_song():
    r = request.get_json()

    song_data = bytes(r.get('song'))

    # Read song metadata
    metadata = MP3(BytesIO(song_data))
    title = metadata.get('TIT2')
    album = metadata.get('TALB')
    artist = metadata.get('TPE1')
    runtime = int(metadata.info.length)

    new_song = Song(
        title=title,
        artist=artist,
        runtime=runtime,
        uploaded_by=core.get_current_user()
    )
