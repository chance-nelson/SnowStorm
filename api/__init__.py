from multiprocessing import Value
from os import chdir, environ

from flask import Flask, Response, current_app, make_response
from flask_cors import CORS

from stream.stream import StreamService
from .stream import STREAM


def create_app(*args):
    app = Flask(__name__)
    CORS(app)

    MUSIC_LIBRARY = environ.get('MUSIC_LIBRARY', './music')

    app.register_blueprint(STREAM)

    app.config['stream'] = StreamService(MUSIC_LIBRARY)

    return app
