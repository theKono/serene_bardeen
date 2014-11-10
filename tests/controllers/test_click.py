#!/usr/bin/env python

# standard library imports
import urllib

# third party related imports
from sure import expect
import ujson

# local library imports
from ..base_test_case import BaseApiTestCase
from ..factories.click import ClickFactory
from serene_bardeen.models.click import Click


# GET /api/clicks
class TestQueryClickEvents(BaseApiTestCase):

    controller = 'serene_bardeen.controllers.click'
    api = '/api/clicks'

    def test_when_spec_is_invalid_json(self):

        params = {'spec': '{}}'}
        response = self.test_app.get(self.api + '?' + urllib.urlencode(params),
                                     expect_errors=True)
        expect(response.status_int).to.eql(400)

    def test_when_fields_is_invalid_json(self):

        params = {'fields': '{}}'}
        response = self.test_app.get(self.api + '?' + urllib.urlencode(params),
                                     expect_errors=True)
        expect(response.status_int).to.eql(400)

    def test_when_limit_is_invalid_integer(self):

        params = {'limit': 'abc'}
        response = self.test_app.get(self.api + '?' + urllib.urlencode(params),
                                     expect_errors=True)
        expect(response.status_int).to.eql(400)

    def test_call_api(self):

        clicks = ClickFactory.create_batch(10)
        spec = {'click_id': {'$gt': clicks[4].click_id}}
        params = {'spec': ujson.dumps(spec)}
        response = self.test_app.get(self.api + '?' + urllib.urlencode(params))
        expect(response.status_int).to.eql(200)
        expect(response.json).to.eql(
            map(lambda c: c.to_json(),
                Click.objects(click_id__gt=clicks[4].click_id).all())
        )

        fields = {'ip': True}
        params = {'fields': ujson.dumps(fields)}
        response = self.test_app.get(self.api + '?' + urllib.urlencode(params))
        expect(response.status_int).to.eql(200)
        expect(response.json).to.eql(
            map(lambda c: {'ip': c.ip}, Click.objects.all())
        )

        response = self.test_app.get(self.api + '?limit=1')
        expect(response.status_int).to.eql(200)
        expect(len(response.json)).to.eql(1)
