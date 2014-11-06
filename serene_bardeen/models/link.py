#!/usr/bin/env python

# standard library imports
import calendar
from datetime import datetime

# third party related imports
from mongoengine import DateTimeField, Document, StringField

# local library imports


class Link(Document):

    article_id = StringField(required=True)
    original_link = StringField(required=True)
    created_at = DateTimeField(required=True, default=datetime.utcnow)

    meta = {
        'indexes': ['article_id', 'original_link']
    }

    def to_json(self):

        return {
            'id': str(self.id),
            'article_id': self.article_id,
            'original_link': self.original_link,
            'created_at': calendar.timegm(self.created_at.timetuple()),
        }
