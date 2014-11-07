#!/usr/bin/env python

# standard library imports

# third party related imports
from bson import ObjectId
from sure import expect

# local library imports
from ..base_test_case import BaseApiTestCase
from ..factories.link import LinkFactory
from serene_bardeen.config import Config
from serene_bardeen.models.link import Link


# POST /links
class TestCreateLink(BaseApiTestCase):

    controller = 'serene_bardeen.controllers.link'
    api = '/api/links'
    secret = Config.SECRET
    original_link = 'http://www.google.com'
    article_id = 'aid'
    params = {
        'secret': secret,
        'original_link': original_link,
        'article_id': article_id
    }

    def test_when_secret_is_incorrect(self):

        params = {'secret': 'incorrect secret'}
        response = self.test_app.post(self.api, params, expect_errors=True)
        expect(response.status_int).to.eql(400)

    def test_when_required_parameter_missed(self):

        params = self.params.copy()
        del params['article_id']
        response = self.test_app.post(self.api, params, expect_errors=True)
        expect(response.status_int).to.eql(400)

        params = self.params.copy()
        del params['original_link']
        response = self.test_app.post(self.api, params, expect_errors=True)
        expect(response.status_int).to.eql(400)

    def test_when_it_is_an_invalid_url(self):

        params = self.params.copy()
        params['original_link'] = 'asdfghjkl'
        response = self.test_app.post(self.api, params, expect_errors=True)
        expect(response.status_int).to.eql(403)

    def test_when_it_looks_like_a_recursive_url(self):

        params = self.params.copy()
        params['original_link'] = 'http://%s/%s' % (Config.DOMAIN_NAME,
                                                    ObjectId())
        response = self.test_app.post(self.api, params, expect_errors=True)
        print response.body
        expect(response.status_int).to.eql(403)

    def test_when_it_is_a_recursive_url(self):

        link = LinkFactory.create()
        params = self.params.copy()
        params['original_link'] = 'http://%s/%s' % (Config.DOMAIN_NAME,
                                                    link.id)
        response = self.test_app.post(self.api, params)
        expect(response.status_int).to.eql(200)
        expect(response.json).to.eql(link.to_json())

    def test_call_api(self):

        response = self.test_app.post(self.api, self.params)
        expect(response.status_int).to.eql(200)
        expect(response.json).to.eql(Link.objects.first().to_json())

        link = Link.objects.first()
        params = self.params.copy()
        params['original_link'] = 'http://%s/%s' % (Config.DOMAIN_NAME,
                                                    link.id)
        response = self.test_app.post(self.api, params)
        expect(response.json).to.eql(link.to_json())
        expect(Link.objects.count()).to.eql(1)
