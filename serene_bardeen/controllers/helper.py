#!/usr/bin/env python

# standard library imports

# third party related imports
import bottle
import ujson

# local library imports


def abort(code=500, body="Unknown Error: Application stopped."):
    """Aborts execution and causes a HTTP error."""

    if isinstance(body, dict):
        raise bottle.HTTPResponse(status=code,
                                  content_type='application/json',
                                  body=ujson.dumps(body, ensure_ascii=False))

    bottle.abort(code, body)


def require_parameter(key):

    if bottle.request.json is not None and key in bottle.request.json:
        return bottle.request.json[key]

    elif bottle.request.params is not None and key in bottle.request.params:
        return bottle.request.params[key]

    else:
        abort(400, {'message': 'Required parameter "%s" missing' % key})
