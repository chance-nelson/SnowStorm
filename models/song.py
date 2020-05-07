from mongoengine import fields

from .entity import Entity


class Song(Entity):
    """Individual songs
    """
    title = fields.StringField()
    album = fields.StringField()
    artist = fields.StringField()
    runtime = fields.IntField()
    bitrate = fields.IntField()
    song = fields.FileField()
