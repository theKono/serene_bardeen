#!/usr/bin/env python

# standard library imports

# third party related imports
from mongoengine import connect
import pymongo

# local library imports
from serene_bardeen.config import Config


def connect_database():

    connect(Config.DB_DATABASE,
            host=Config.DB_HOST,
            username=Config.DB_USERNAME,
            password=Config.DB_PASSWORD)


def get_pymongo_db():

    client = pymongo.MongoClient(Config.DB_HOST)

    if Config.DB_USERNAME and Config.DB_PASSWORD:
        client.authenticate(Config.DB_USERNAME, Config.DB_PASSWORD)

    return client[Config.DB_DATABASE]
