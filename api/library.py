from flask import Response, current_app, make_response, Blueprint, jsonify


STREAM = Blueprint('stream', __name__, url_prefix='/stream')


@STREAM.route('/skip')
def skip():
    current_app.config.get('stream').skip()
    return make_response('', 200)


@STREAM.route('/stream.mp3')
def stream():
    return Response(current_app.config.get('stream').listen(),
                    mimetype='audio/mpeg')

@STREAM.route('/')
def get_playing():
    title = current_app.config.get('stream').title.value.decode()
    artist = current_app.config.get('stream').artist.value.decode()
    return make_response(jsonify({'title': title, 'artist': artist}), 200)
