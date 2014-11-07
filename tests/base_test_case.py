#!/usr/bin/env python

# standard library imports

# third party related imports
import unittest2
from webtest import TestApp

# local library imports
from serene_bardeen.models import connect_database, get_pymongo_db


class BaseTestCase(unittest2.TestCase):

    pass


class BaseDbTestCase(BaseTestCase):

    def setUp(self):

        super(BaseDbTestCase, self).setUp()
        connect_database()

    def tearDown(self):

        self._nuke_db()
        super(BaseDbTestCase, self).tearDown()

    def _nuke_db(self):

        db = get_pymongo_db()
        map(lambda c: db[c].remove({}, multi=True),
            db.collection_names(include_system_collections=False))


class BaseApiTestCase(BaseDbTestCase):

    def setUp(self):

        super(BaseApiTestCase, self).setUp()

        if getattr(self, 'controller', None) is not None:
            ctrl_module = __import__(self.controller, fromlist=['app'])
            self.test_app = TestApp(ctrl_module.app)
