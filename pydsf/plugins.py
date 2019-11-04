# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging
from suds.plugin import MessagePlugin


class LogPlugin(MessagePlugin):

    def __init__(self, logger_name):
        self.logger_name = logger_name

    def sending(self, context):
        logger = logging.getLogger(self.logger_name)
        logger.info(unicode(context.envelope))

    def received(self, context):
        logger = logging.getLogger(self.logger_name)
        logger.info(unicode(context.reply))
