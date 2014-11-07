#!/usr/bin/env python

# standard library imports

# third party related imports
import unittest2

# local library imports
from serene_bardeen.models import connect_database, get_pymongo_db


class BaseTestCase(unittest2.TestCase):

    pass


class BaseDbTestCase(BaseTestCase):

    def setUp(self):

        connect_database()

    def tearDown(self):

        self._nuke_db()

    def _nuke_db(self):

        db = get_pymongo_db()
        collections = db.collection_names(include_system_collections=False)
        map(lambda c: c.remove({}, multi=True), collections)
