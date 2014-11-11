#!/usr/bin/env python

# standard library imports

# third party related imports
from bson import ObjectId
from factory import Sequence
from factory.mongoengine import MongoEngineFactory

# local library imports
from serene_bardeen.models.link import Link


class LinkFactory(MongoEngineFactory):

    FACTORY_FOR = Link

    id = Sequence(lambda _: ObjectId())
    article_id = Sequence(lambda n: 'aid%s' % n)
    original_link = Sequence(lambda n: 'http://www.google.com?go=%s' % n)
