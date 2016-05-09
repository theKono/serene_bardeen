#!/usr/bin/env python

# FIXME change the activate_this script path
virtualenv_script = '/opt/serene_bardeen/bin/activate_this.py'
execfile(virtualenv_script, dict(__file__=virtualenv_script))

# standard library imports
import os

# FIXME change to a non-writable by group directory
os.environ['PYTHON_EGG_CACHE'] = '/var/www/serene.thekono.com/python-egg'

# third party related imports
from bottle import Bottle

# local libary imports
from serene_bardeen.controllers.click import app as click_ctrl
from serene_bardeen.controllers.link import app as link_ctrl
from serene_bardeen.models import connect_database


connect_database()
application = Bottle()
application.merge(click_ctrl)
application.merge(link_ctrl)

