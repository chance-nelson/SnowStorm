from flask import Flask
from flask_cors import CORS
from mongoengine import connect
from os import environ

from stream.stream import StreamService
from .stream import STREAM
from .library import LIBRARY


def create_app(*args, **kwargs):
    app = Flask(__name__)
    CORS(app)

    connection_args = {
        'db': environ.get('DB_NAME', 'snowstorm'),
        'host': environ.get('DB_HOST'),
    }

    app.config['DB'] = connect(**connection_args)

    app.register_blueprint(STREAM)
    app.register_blueprint(LIBRARY)

    app.config['stream'] = StreamService(mongo_args=connection_args)

    return app
