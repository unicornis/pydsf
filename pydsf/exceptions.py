# -*- coding: utf-8 -*-
from __future__ import unicode_literals


class DSFException(Exception):
    pass


class DSFClientError(DSFException):
    pass


class DSFInputError(DSFException):
    pass


class InvalidServiceUrlError(DSFException):
    pass


class InvalidUsernameError(DSFException):
    pass


class InvalidPasswordError(DSFException):
    pass


class InvalidSystemNameError(DSFException):
    pass


class DSFServiceError(DSFException):
    pass
