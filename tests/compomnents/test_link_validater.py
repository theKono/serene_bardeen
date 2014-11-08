#!/usr/bin/env python

# standard library imports

# third party related imports
from bson import ObjectId
from sure import expect

# local library imports
from ..base_test_case import BaseTestCase
from serene_bardeen.components.link_validater import LinkValidater
from serene_bardeen.config import Config


class TestLinkValidater(BaseTestCase):

    def test_is_valid_url(self):

        url = 'file:///tmp/xxx.txt'
        lv = LinkValidater(url)
        expect(lv.is_valid_url()).to.be(False)

        url = 'asdfghjkl'
        lv = LinkValidater(url)
        expect(lv.is_valid_url()).to.be(False)

        url = 'http://tw.yahoo.com'
        lv = LinkValidater(url)
        expect(lv.is_valid_url()).to.be(True)

        url = 'https://www.google.com'
        lv = LinkValidater(url)
        expect(lv.is_valid_url()).to.be(True)

    def test_may_recursive(self):

        url = 'file:///tmp/xxx.txt'
        lv = LinkValidater(url)
        expect(lv.may_recursive()).to.be(False)

        url = 'http://%s' % (Config.DOMAIN_NAME)
        lv = LinkValidater(url)
        expect(lv.may_recursive()).to.be(False)

        url = 'http://%s/%s' % (Config.DOMAIN_NAME, ObjectId())
        lv = LinkValidater(url)
        expect(lv.may_recursive()).to.be(True)

        url = 'https://%s/%s/' % (Config.DOMAIN_NAME, ObjectId())
        lv = LinkValidater(url)
        expect(lv.may_recursive()).to.be(True)

    def test_get_link_id(self):

        url = 'asdfghjkl'
        lv = LinkValidater(url)
        expect(lv.get_link_id()).to.be(None)

        oid = str(ObjectId())
        url = 'http://%s/%s' % (Config.DOMAIN_NAME, oid)
        lv = LinkValidater(url)
        expect(lv.get_link_id()).to.eql(oid)

        oid = str(ObjectId())
        url = 'https://%s/%s/' % (Config.DOMAIN_NAME, oid)
        lv = LinkValidater(url)
        expect(lv.get_link_id()).to.eql(oid)
