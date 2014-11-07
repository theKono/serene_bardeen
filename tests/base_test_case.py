#!/usr/bin/env python

# standard library imports
import os.path
import shutil

# third party related imports
import unittest2

# local library imports
from serene_bardeen.config import Config


class BaseTestCase(unittest2.TestCase):

    def setUp(self):

        self._create_test_config()

    def tearDown(self):

        self._nuke_db()
        self._remove_test_config()

    def _nuke_db(self):

        pass

    @property
    def _pkg_dir(self):

        cwd = os.path.abspath(os.path.dirname(__file__))
        return os.path.join(cwd, '..', 'serene_bardeen')

    def _create_test_config(self):

        shutil.copy(os.path.join(self._pkg_dir, 'config_test.py'),
                    os.path.join(self._pkg_dir, 'config.py'))

    def _remove_test_config(self):

        pass
