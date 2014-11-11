#!/usr/bin/env python

# standard library imports

# third party related imports
from bottle import Bottle, request, response
import ujson

# local library imports
from serene_bardeen.controllers.helper import abort
from serene_bardeen.models import get_pymongo_db
from serene_bardeen.models.click import Click


app = Bottle()


@app.get('/api/clicks')
def query():

    try:
        spec = ujson.loads(request.params.get('spec', 'null'))
        fields = ujson.loads(request.params.get('fields', 'null'))
        limit = max(0, int(request.params.get('limit', '100')))
    except ValueError:
        abort(400, {'message': 'Invalid json'})

    db = get_pymongo_db()
    cursor = db.click.find(spec=spec, fields=fields, limit=limit)

    response.content_type = 'application/json'
    return ujson.dumps(map(Click.from_pymongo_to_json, cursor))
