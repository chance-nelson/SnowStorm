from datetime import datetime
from uuid import uuid4

from mongoenine import Document, fields


class Entity(Document):
    meta = {
        'abstract': True,
    }

    id = fields.UUIDField(primary_key=True, default=lambda: uuid4())
    create_time = fields.DateTimeField(default=lambda: datetime.now())
    inactive = fields.BooleanField(default=False)


class User(Entity):
    username = fields.StringField()
    password = fields.StringField()


class Song(Entity):
    """Individual songs
    """
    title = fields.StringField()
    album = fields.StringField()
    artist = fields.StringField()
    runtime = fields.IntField()
    bitrate = fields.IntField()
    song = fields.FileField()
