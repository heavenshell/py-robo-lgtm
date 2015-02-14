# -*- coding: utf-8 -*-
"""
    robo.tests.test_lgtm_handler
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Tests for robo.handlers.lgtm.


    :copyright: (c) 2015 Shinya Ohyanagi, All rights reserved.
    :license: BSD, see LICENSE for more details.
"""
import os
import logging
import requests
from mock import patch
from unittest import TestCase
from robo.robot import Robot
from robo.handlers.lgtm import Client, Lgtm


def dummy_response(m, filename=None):
    response = requests.Response()
    response.status_code = 200
    if filename is None:
        response._content = ''
    else:
        root_path = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(root_path, filename)
        with open(file_path, 'r') as f:
            data = f.read()
        response._content = data

    m.return_value = response


class NullAdapter(object):
    def __init__(self, signal):
        self.signal = signal
        self.responses = []

    def say(self, message, **kwargs):
        self.responses.append(message)
        return message


class TestClient(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = Client()

    @patch('robo.handlers.lgtm.requests.get')
    def test_generate_url(self, m):
        """ Client().generate() should generate http://lgtm.herokuapp.com url. """
        dummy_response(m, 'fixture.json')
        ret = self.client.generate('cat')
        self.assertRegexpMatches(ret, r'^http://lgtm.herokuapp.com/http://')

    @patch('robo.handlers.lgtm.requests.get')
    def test_search_resource(self, m):
        """ Client().search_resource() should search tumblr. """
        dummy_response(m, 'fixture.json')
        ret = self.client.search_resource('cat')
        self.assertTrue(isinstance(ret, dict))
        self.assertTrue('tumblr' in ret['unescapedUrl'])


class TestLgtmHandler(TestCase):
    @classmethod
    def setUpClass(cls):
        logger = logging.getLogger('robo')
        logger.level = logging.ERROR
        cls.robot = Robot('test', logger)

        lgtm = Lgtm()
        lgtm.signal = cls.robot.handler_signal
        method = cls.robot.parse_handler_methods(lgtm)
        cls.robot.handlers.extend(method)

        adapter = NullAdapter(cls.robot.handler_signal)
        cls.robot.adapters['null'] = adapter

    @patch('robo.handlers.lgtm.requests.get')
    def test_should_lgtm(self, m):
        """ Lgtm().get() should search lgtm url. """
        dummy_response(m, 'fixture.json')
        self.robot.handler_signal.send('test lgtm')
        self.assertRegexpMatches(self.robot.adapters['null'].responses[0],
                                 r'^http://lgtm.herokuapp.com/http://*')
        self.robot.adapters['null'].responses = []
