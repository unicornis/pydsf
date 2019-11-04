# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging
from logging.handlers import TimedRotatingFileHandler
import os

import validators
from suds.client import Client

from .config import DISTRIBUTION_CHANNEL, SESSION_HEADER, TRANSACTION_HEADER, DEFAULT_LOG_FORMAT, LOGGER_NAME
from .exceptions import DSFClientError, InvalidServiceUrlError, InvalidUsernameError, \
    InvalidPasswordError, InvalidSystemNameError
from .plugins import LogPlugin
from pydsf.service.person import find_person


class DSFClient(object):

    """
    A client to interface with Det Sentrale Folkeregister.
    """

    _suds = None
    _service_url = None
    _username = None
    _password = None
    _system_name = None

    def __init__(self, url, username, password, system_name, show_details=False, show_response_time=False,
                 show_raw=False, log_level=logging.INFO, log_format=DEFAULT_LOG_FORMAT,
                 log_location='/tmp/pydsf', log_rollover='midnight'):
        self.service_url = url
        self.username = username
        self.password = password
        self.system_name = system_name
        self.show_details = show_details
        self.show_response_time = show_response_time
        self.show_raw = show_raw
        self.log_level = log_level
        self.log_format = log_format
        self.log_location = log_location
        self.log_rollover = log_rollover

        self._build_client()

    @property
    def service_url(self):
        """ The WSDL location for this service. """
        return self._service_url

    @service_url.setter
    def service_url(self, value):
        if not value:
            raise InvalidServiceUrlError('Service url is required')
        service_url = unicode(value)
        if not validators.url(service_url):
            raise InvalidServiceUrlError('{} is not a valid url'.format(service_url))
        self._service_url = service_url

    @property
    def username(self):
        return self._username

    @username.setter
    def username(self, value):
        if not value:
            raise InvalidUsernameError('Username is required.')
        self._username = unicode(value)

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, value):
        if not value:
            raise InvalidPasswordError('Password is required.')
        self._password = unicode(value)

    @property
    def system_name(self):
        return self._system_name

    @system_name.setter
    def system_name(self, value):
        if not value:
            raise InvalidSystemNameError('System name is required')
        self._system_name = unicode(value)

    def _build_client(self, faults=False):
        """
        Build a workable client.

        This function checks for a valid configuration and tries to set up a Suds SOAP client
        that can be called on later.

        Raises:
            DSFClientError: If there was a problem assmebling the client.

        """
        log = self.get_logger()
        client_args = {
            "url": self.service_url,
            "faults": faults,
            'plugins': [LogPlugin(LOGGER_NAME)]
        }
        log.info("Setting up client at {}".format(self.service_url))
        try:
            client = Client(**client_args)
        except BaseException as error:
            err_prefix = ("Could not create SOAP client. This could mean that"
                          "the server responded with regular HTML. ")
            err_msg = "Please check the url: {0}. Error message: {1}".format(client_args["url"],
                                                                             error)
            log.error(err_msg)
            import traceback
            log.error(traceback.format_exc())
            raise DSFClientError(err_prefix + err_msg)

        session_args = {
            'brukernavn': self.username,
            'distribusjonskanal': DISTRIBUTION_CHANNEL,
            'passord': self.password,
            'systemnavn': self.system_name
        }
        session_header = self.create_header(client, SESSION_HEADER, session_args)
        transaction_args = {
            'visDetaljer': self.show_details,
            'visResponstid': self.show_response_time,
            'visRaadata': self.show_raw
        }
        transaction_header = self.create_header(client, TRANSACTION_HEADER, transaction_args)
        client.set_options(soapheaders=(session_header, transaction_header))
        log.debug('SOAP client setup complete.')
        self._suds = client

    def get_logger(self):
        log = logging.getLogger(LOGGER_NAME)

        if len(log.handlers) != 0:
            return log

        log.setLevel(self.log_level)
        if not os.path.exists(self.log_location):
            os.makedirs(self.log_location)
        log_file = os.path.join(self.log_location, '{}.log'.format(LOGGER_NAME))

        file_handler = TimedRotatingFileHandler(log_file, when=self.log_rollover)
        file_handler.setLevel(self.log_level)
        file_handler.setFormatter(logging.Formatter(self.log_format))
        log.addHandler(file_handler)
        return log

    def create_header(self, client, element_name, fields):
        log = self.get_logger()
        log.info('Setting header: {header}'.format(header=element_name))
        try:
            header = client.factory.create(element_name)
        except (TypeError, Exception) as error:
            err_msg = error.message
            log.error(error.message)
            import traceback
            log.error(traceback.format_exc())
            err_prefix = 'Namespace {ns} is not available on this service'.format(ns=element_name)
            raise DSFClientError(' '.join((err_prefix, err_msg)))

        for field_name, value in fields.iteritems():
            setattr(header, field_name, value)

        return header

    def get_details(self, **search_args):
        """
        Straight passthrough of HentDetaljer from this service.
        """
        return self._suds.service.hentDetaljer(**search_args)

    def find_person(self, **search_args):
        """
        Uses service function to validate and parse input and output.
        """
        return find_person(self, **search_args)
