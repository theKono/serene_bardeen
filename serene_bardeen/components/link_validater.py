#!/usr/bin/env python

# standard library imports
import re
from urlparse import urlparse

# third party related imports

# local library imports
from serene_bardeen.config import Config


class LinkValidater(object):

    ID_PATTERN = re.compile('[0-9a-f]{24}', re.IGNORECASE)
    PATH_PATTERN = re.compile('^/[0-9a-f]{24}/?$', re.IGNORECASE)

    def __init__(self, url):

        self.url = url
        self.parse_result = None

    def is_valid_url(self):

        try:
            self.parse_result = urlparse(self.url)
            return True
        except Exception:
            return False

    def may_recursive(self):

        if self.parse_result is None:
            if not self.is_valid_url():
                return False

        if self.parse_result.netloc == Config.DOMAIN_NAME:
            if self.PATH_PATTERN.match(self.parse_result.path):
                return True

        return False

    def get_link_id(self):

        if not self.may_recursive():
            return None

        return self.ID_PATTERN.search(self.parse_result.path).group()
