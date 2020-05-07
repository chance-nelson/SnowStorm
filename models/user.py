from mongoengine import fields

from .entity import Entity


class User(Entity):
    username = fields.StringField()
    password = fields.StringField()
