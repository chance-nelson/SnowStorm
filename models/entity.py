from datetime import datetime
from uuid import uuid4

from mongoengine import Document, fields


class Entity(Document):
    meta = {
        'abstract': True,
    }

    id = fields.UUIDField(primary_key=True, default=lambda: uuid4())
    create_time = fields.DateTimeField(default=lambda: datetime.now())
    inactive = fields.BooleanField(default=False)
