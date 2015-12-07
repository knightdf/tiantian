# coding=utf-8
import logging
import logging.config


logging.config.fileConfig('log/logger.conf')
log1 = logging.getLogger('wechat')

class Logger(object):

    @staticmethod
    def debug(msg, name=None):
        log1.debug(msg)

    @staticmethod
    def log(msg, name=None):
        log1.info(msg)

    @staticmethod
    def error(msg, name=None):
        log1.error(msg)
