# -*- coding: utf-8 -*-
"""
    robo.tests.test_cron
    ~~~~~~~~~~~~~~~~~~~~

    Tests for robo.handlers.cron.


    :copyright: (c) 2015 Shinya Ohyanagi, All rights reserved.
    :license: BSD, see LICENSE for more details.
"""
import logging
from unittest import TestCase
from robo.robot import Robot
from robo.handlers.lgtm import Client, Lgtm


class NullAdapter(object):
    def __init__(self, signal):
        self.signal = signal
        self.responses = []

    def say(self, message, **kwargs):
        self.responses.append(message)
        return message


class TestScheduler(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = Client()

    def test_generate_url(self):
        """ Client().generate() should generate http://lgtm.herokuapp.com url. """
        ret = self.client.generate('cat')
        self.assertRegexpMatches(ret, r'^http://lgtm.herokuapp.com/http://')

    def test_search_resource(self):
        """ Client().search_resource() should search tumblr. """
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

    def test_should_lgtm(self):
        """ Lgtm().get() should search lgtm url. """
        self.robot.handler_signal.send('test lgtm')
        self.assertRegexpMatches(self.robot.adapters['null'].responses[0],
                                 r'^http://lgtm.herokuapp.com/http://*')
        self.robot.adapters['null'].responses = []
