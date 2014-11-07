#!/usr/bin/env python

# standard library imports

# third party related imports
from mongoengine import connect
import pymongo

# local library imports
from serene_bardeen.config import Config


def connect_database():

    connect(Config.DB_DATABASE,
            Config.DB_HOST,
            username=Config.DB_USERNAME,
            password=Config.DB_PASSWORD)


def get_pymongo_db():

    client = pymongo.MongoClient('mongodb://%s:%s@%s' % (Config.DB_USERNAME,
                                                         Config.DB_PASSWORD,
                                                         Config.DB_HOST))
    return client[Config.DB_DATABASE]
