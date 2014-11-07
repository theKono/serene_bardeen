#!/usr/bin/env python

# standard library imports

# third party related imports
from bottle import Bottle
from mongoengine import NotUniqueError

# local library imports
from serene_bardeen.components.link_validater import LinkValidater
from serene_bardeen.controllers.helper import abort, require_parameter
from serene_bardeen.config import Config
from serene_bardeen.models.link import Link


app = Bottle()


@app.post('/links')
def create():

    if require_parameter('secret') != Config.SECRET:
        abort(400, {'message': 'Authorization error'})

    original_link = require_parameter('original_link')
    validater = LinkValidater(original_link)

    if not validater.is_valid_url():
        abort(403, {'message': 'Invalid url'})

    if validater.may_recursive():
        link = Link.objects(id=validater.get_link_id()).first()

        if link is None:
            abort(403, {'message': 'Invalid recursive url'})

        return link.to_json()

    link = Link(article_id=require_parameter('article_id'),
                original_link=original_link)

    try:
        link.save()
    except NotUniqueError:
        link = Link.objects(original_link=original_link).first()

    return link.to_json()
