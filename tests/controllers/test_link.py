#!/usr/bin/env python

# standard library imports

# third party related imports
from bson import ObjectId
from sure import expect

# local library imports
from ..base_test_case import BaseApiTestCase
from ..factories.link import LinkFactory
from serene_bardeen.config import Config
from serene_bardeen.models.click import Click
from serene_bardeen.models.link import Link


# POST /api/links
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


# GET /<link_id>
class TestRedirectOriginalLink(BaseApiTestCase):

    controller = 'serene_bardeen.controllers.link'

    def test_when_link_does_not_exist(self):

        response = self.test_app.get('/%s' % ObjectId(), expect_errors=True)
        expect(response.status_int).to.eql(404)

    def test_when_link_exists(self):

        link = LinkFactory.create()
        ip = '69.181.253.158'
        user_agent = 'Testing'
        headers = {'X-Real-Ip': ip, 'X-User-Agent': user_agent}

        response = self.test_app.get('/%s' % link.id, headers=headers)
        expect(response.status_int in (302, 303)).to.be(True)
        expect(response.location).to.equal(link.original_link)

        click_event = Click.objects.first()
        expect(click_event).to_not.be(None)
        expect(click_event.link_id).to.eql(link.id)
        expect(click_event.ip).to.eql(Click.ip2long(ip))
        expect(click_event.user_agent).to.eql(user_agent)
