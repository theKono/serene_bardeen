#!/usr/bin/env python

# standard library imports
import calendar
from datetime import datetime

# third party related imports
from mongoengine import DateTimeField, Document, StringField

# local library imports
from serene_bardeen.config import Config


class Link(Document):

    article_id = StringField(required=True, unique_with='original_link')
    original_link = StringField(required=True)
    created_at = DateTimeField(required=True, default=datetime.utcnow)

    def to_json(self):

        return {
            'id': str(self.id),
            'article_id': self.article_id,
            'original_link': self.original_link,
            'created_at': calendar.timegm(self.created_at.timetuple()),
            'short_link': 'http://%s/%s' % (Config.DOMAIN_NAME, self.id)
        }
