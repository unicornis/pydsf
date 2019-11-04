# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import unittest

import mock

from pydsf.exceptions import InvalidServiceUrlError, InvalidUsernameError, InvalidPasswordError, \
    InvalidSystemNameError
from pydsf.client import DSFClient

URL = 'http://example.com'
USER = 'username'
PASSWORD = 'password'
SYSTEM_NAME = 'system_name'


class ClientTests(unittest.TestCase):

    def setUp(self):
        pass

    def test_service_url(self):
        bad_inputs = [None, '', 'notaurl']
        for val in bad_inputs:
            args = (val, USER, PASSWORD, SYSTEM_NAME)
            with self.assertRaises(InvalidServiceUrlError):
                DSFClient(*args)

    def test_username(self):
        bad_inputs = [None, '']
        for val in bad_inputs:
            args = (URL, val, PASSWORD, SYSTEM_NAME)
            with self.assertRaises(InvalidUsernameError):
                DSFClient(*args)

    def test_password(self):
        bad_inputs = [None, '']
        for val in bad_inputs:
            args = (URL, USER, val, SYSTEM_NAME)
            with self.assertRaises(InvalidPasswordError):
                DSFClient(*args)

    def test_system_name(self):
        bad_inputs = [None, '']
        for val in bad_inputs:
            args = (URL, USER, PASSWORD, val)
            with self.assertRaises(InvalidSystemNameError):
                DSFClient(*args)

    @mock.patch("pydsf.client.Client", side_effect=lambda x: Exception())
    def test_build_client_with_error(self, mocked):
        pass

    def test_get_logger(self):
        pass
