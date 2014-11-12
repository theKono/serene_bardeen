#!/usr/bin/env python

# standard library imports
from random import randint

# third party related imports
from bson import ObjectId
from factory import Sequence
from factory.mongoengine import MongoEngineFactory

# local library imports
from serene_bardeen.models.click import Click


def randip():

    return '.'.join(map(lambda _: str(randint(0, 255)), xrange(4)))


class ClickFactory(MongoEngineFactory):

    FACTORY_FOR = Click

    id = Sequence(lambda _: str(ObjectId()))
    link_id = Sequence(lambda _: str(ObjectId()))
    article_id = Sequence(lambda n: 'aid_%s' % n)
    original_link = Sequence(lambda n: 'http://www.google.com?q=%s' % n)
    ip = Sequence(lambda _: randip())
    user_agent = Sequence(lambda n: 'user-agent %s' % n)
