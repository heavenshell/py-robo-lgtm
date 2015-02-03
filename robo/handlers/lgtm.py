# -*- coding: utf-8 -*-
"""
    robo.handlers.lgtm
    ~~~~~~~~~~~~~~~~~~

    LGTM.


    :copyright: (c) 2015 Shinya Ohyanagi, All rights reserved.
    :license: BSD, see LICENSE for more details.
"""
import random
import requests
import simplejson as json
from robo.decorators import cmd


class Client(object):
    #: Add LGTM word to animation gif.
    DEFAULT_ENDPOINT = 'http://lgtm.herokuapp.com'

    #: Search animation gif from tumblr.
    GOOGLE_IMAGE_URL = 'http://ajax.googleapis.com/ajax/services/search/images'

    def __init__(self):
        self.resource = None

    def generate(self, query=None):
        """Generate lgtm uri.

        :param query: Search query
        """
        if query is None:
            query = 'cat'
        url = self.search_resource(query)
        if url:
            return '{0}/{1}'.format(self.DEFAULT_ENDPOINT, url['unescapedUrl'])

    def search_resource(self, query):
        """Search image resource using Google site-search.

        :param query:
        """
        if self.resource is None:
            params = {
                'rsz': 8,
                'safe': 'active',
                'v': '1.0',
                'as_filetype': 'gif',
                'imgsz': 'large',
                'as_sitesearch': 'tumblr.com',
                'q': query
            }

            res = requests.get(self.GOOGLE_IMAGE_URL, params=params)
            if res.status_code == 200:
                body = json.loads(res.content)
                self.resource = random.choice(body['responseData']['results'])

        return self.resource


class Lgtm(object):
    def __init__(self):
        self.client = Client()

    @cmd(regex=r'lgtm( me)? ?(?P<keyword>.+)?',
         description='Generate lgtm image matching with the keyword.')
    def get(self, message, **kwargs):
        return self.client.generate(message.match.group(1))
