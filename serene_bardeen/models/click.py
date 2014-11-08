#!/usr/bin/env python

# standard library imports
import socket
import struct
import time

# third party related imports
from mongoengine import Document, IntField, ObjectIdField, StringField

# local library imports


class Click(Document):

    link_id = ObjectIdField(required=True)
    ip = IntField(required=True)
    user_agent = StringField(required=True)
    created_at = IntField(required=True, default=time.time)

    meta = {
        'indexes': ['link_id', 'created_at']
    }

    @classmethod
    def ip2long(cls, ip):

        return struct.unpack("!L", socket.inet_aton(ip))[0]

    @classmethod
    def long2ip(cls, longip):

        return socket.inet_ntoa(struct.pack('>L', longip))

    def to_json(self):

        return {
            'id': str(self.id),
            'link': str(self.link_id),
            'ip': self.long2ip(self.ip),
            'user_agent': self.user_agent,
            'created_at': self.created_at,
        }
