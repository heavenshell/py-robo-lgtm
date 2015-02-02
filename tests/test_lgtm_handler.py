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


#class TestLgtmHandler(TestCase):
#    @classmethod
#    def setUpClass(cls):
#        logger = logging.getLogger('robo')
#        logger.level = logging.ERROR
#        cls.robot = Robot('test', logger)
#
#        lgtm = Lgtm()
#        lgtm.signal = cls.robot.handler_signal
#        method = cls.robot.parse_handler_methods(lgtm)
#        cls.robot.handlers.extend(method)
#
#        adapter = NullAdapter(cls.robot.handler_signal)
#        cls.robot.adapters['null'] = adapter
#
