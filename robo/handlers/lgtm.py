# -*- coding: utf-8 -*-
"""
    robo.handlers.lgtm
    ~~~~~~~~~~~~~~~~~~

    LGTM.

    Porting from `ruboty-lgtm <https://github.com/negipo/ruboty-lgtm>`_.


    :copyright: (c) 2016 Shinya Ohyanagi, All rights reserved.
    :license: BSD, see LICENSE for more details.
"""
import logging
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
        pass

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
        params = {
            'rsz': 8,
            'safe': 'active',
            'v': '1.0',
            'as_filetype': 'gif',
            'imgsz': 'large',
            'as_sitesearch': 'tumblr.com',
            'q': query
        }

        resource = None
        res = requests.get(self.GOOGLE_IMAGE_URL, params=params)
        print(res.content)
        if res.status_code == 200:
            body = json.loads(res.content)
            resource = random.choice(body['responseData']['results'])

        return resource


class Lgtm(object):
    def __init__(self):
        #: Change requests log level.
        logging.getLogger('requests').setLevel(logging.ERROR)
        self.client = Client()

    @cmd(regex=r'lgtm( me)? ?(?P<keyword>.+)?',
         description='Generate lgtm image matching with the keyword.')
    def get(self, message, **kwargs):
        return self.client.generate(message.match.group(1))
