#!/usr/bin/env python

# standard library imports

# third party related imports
from sure import expect

# local library imports
from ..base_test_case import BaseDbTestCase
from ..factories.click import ClickFactory
from serene_bardeen.models.click import Click


class TestClickModel(BaseDbTestCase):

    def test_ip2long_long2ip(self):

        ip = '67.188.29.148'
        expect(Click.long2ip(Click.ip2long(ip))).to.eql(ip)

    def test_pre_save(self):

        click = ClickFactory.build()
        click.save()
        expect(click.click_id).to.eql(str(click.id))

