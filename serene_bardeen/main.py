#!/usr/bin/env python

# standard library imports

# third party related imports
from bottle import Bottle

# local library imports
from serene_bardeen.controllers.click import app as click_ctrl
from serene_bardeen.controllers.link import app as link_ctrl
from serene_bardeen.models import connect_database


connect_database()
application = Bottle()
application.merge(click_ctrl)
application.merge(link_ctrl)
