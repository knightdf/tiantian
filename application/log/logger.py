# coding=utf-8

import logging
from logging.handlers import SMTPHandler
from handlers import MultiProcessTimedRotatingFileHandler
from application import config


_Levels = {
    'DEBUG': logging.DEBUG,
    'INFO': logging.INFO,
    'WARN': logging.WARN,
    'WARNING': logging.WARNING,
    'ERROR': logging.ERROR,
    'CRITICAL': logging.CRITICAL
    }

log = logging.getLogger('wechat')
log.setLevel(_Levels.get(str.upper(config.LogLevel or ''), logging.NOTSET))
log.propagate = False

__h1 = MultiProcessTimedRotatingFileHandler(config.LogPath or 'wechat.log', 'midnight')
__h1.setLevel(logging.DEBUG)

__f = logging.Formatter('%(asctime)s [%(name)s] %(levelname)s: %(message)s')
__h1.setFormatter(__f)

if config.MailNotifyEnable:
    __h2 = SMTPHandler(config.MailHost, config.MailFrom, config.MailTo,\
            'New Critical Event From [WeChat: TianTian]', (config.MailFrom, config.MailPass))
    __h2.setLevel(logging.CRITICAL)
    __h2.setFormatter(__f)
    log.addHandler(__h2)

log.addHandler(__h1)


if __name__ == '__main__':
    log.debug('debug message')
    log.info('info message')
    log.warn('warn message')
    log.error('error message')
    log.critical('critical message')
