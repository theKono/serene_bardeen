#!/usr/bin/env python

# standard library imports
import socket
import struct
import time

# third party related imports
from bson import ObjectId
from mongoengine import Document, IntField, StringField
from mongoengine import signals

# local library imports


class Click(Document):

    # same as _id, but type is str
    click_id = StringField(required=True, unique=True)
    link_id = StringField(required=True)
    article_id = StringField(required=True)
    original_link = StringField(required=True)
    ip = StringField(required=True)
    user_agent = StringField(required=True)
    created_at = IntField(required=True, default=time.time)

    meta = {
        'indexes': ['link_id', 'article_id', 'created_at']
    }

    permitted_fields = (
        'click_id', 'link_id', 'article_id', 'original_link',
        'ip', 'user_agent', 'created_at'
    )

    @classmethod
    def ip2long(cls, ip):

        return struct.unpack("!L", socket.inet_aton(ip))[0]

    @classmethod
    def long2ip(cls, longip):

        return socket.inet_ntoa(struct.pack('>L', longip))

    @classmethod
    def from_pymongo_to_json(cls, doc):

        return {k: doc[k] for k in cls.permitted_fields if k in doc}

    @classmethod
    def pre_save(cls, sender, document, **kwargs):

        if document.click_id is None:
            if document.id is None:
                document.id = ObjectId()

            document.click_id = str(document.id)

    def to_json(self):

        return {pf: getattr(self, pf, None) for pf in self.permitted_fields}


signals.pre_save.connect(Click.pre_save, sender=Click)
