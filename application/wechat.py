# coding=utf-8

from wechat_sdk import (WechatBasic, WechatExt)
from log.logger import log
import config
import fcntl
import os
import json
import time


class Wechat(WechatBasic):
    """cache access_token and jsapi_ticket at local(file/db/redis/3rd service)"""

    def __init__(self):
        super(Wechat, self).__init__(\
                config.Token,\
                config.AppID,\
                config.AppSecret
                )

    def _get_cache(self, mode='r'):
        """
        get reference of source where cache stored
        :return: file discriptor
        """

        _file_name = '.cache'
        if not os.path.exists(_file_name):
            return open(_file_name, 'w+')
        return open(_file_name, mode)

    def _load_cache(self):
        """
        get cached value of access_token and jsapi_ticket
        :return: dict
        """

        f = self._get_cache()
        fcntl.flock(f, fcntl.LOCK_SH)
        cache = {}
        try:
            cache = json.loads(f.read() or '{}')
            if not isinstance(cache, dict):
                #raise ValueError('Bad data in cache.')
                cache = {}
        except Exception, e:
            log.error('Bad data in cache! Please check cached data.\nError: %s'%e)
        finally:
            fcntl.flock(f, fcntl.LOCK_UN)
            f.close()
        return cache

    def _update_cache(self, token):
        """
        update value of access_token or jsapi_ticket in cache
        :params
            token: a dict contains 'access_token' or 'ticket'
                with the same struct returned by wechat offical api
        """

        if not isinstance(token, dict):
            raise TypeError('The given token must be a dict.')

        access_token = token.has_key('access_token') and token
        jsapi_ticket = token.has_key('ticket') and token

        # value check
        if not (access_token or jsapi_ticket):
            raise ValueError('At least one of ("access_token", "jsapi_ticket") should be given in dict.')
        if access_token and not access_token.has_key('expires_in'):
            raise ValueError('Bad value of access_token: %s'%str(access_token))
        if jsapi_ticket and not jsapi_ticket.has_key('expires_in'):
            raise ValueError('Bad value of jsapi_ticket: %s'%str(jsapi_ticket))

        # read old value and update
        f = self._get_cache('r+')
        fcntl.flock(f, fcntl.LOCK_EX)
        try:
            # read old data
            cache = json.loads(f.read() or '{}')
            if not isinstance(cache, dict):
                #raise ValueError('Bad data in cache.')
                cache = {}
            if access_token:
                access_token['expires_at'] = int(time.time()) + access_token.get('expires_in')
                cache['access_token'] = access_token
            if jsapi_ticket:
                jsapi_ticket['expires_at'] = int(time.time()) + jsapi_ticket.get('expires_in')
                cache['jsapi_ticket'] = jsapi_ticket
            # write new data
            f.seek(0)
            f.truncate()
            f.write(json.dumps(cache))
        except Exception, e:
            log.error('Update cache error: %s'%e)
        finally:
            fcntl.flock(f, fcntl.LOCK_UN)
            f.close()

    def _cache_expired(self, token):
        """check expiration of token in cache"""

        now = time.time()
        if now - token.get('expires_at') > -60:
            log.debug('token in cache was expired')
            return True
        return False

    def grant_token(self, override=True):
        """grant token from cache first, then from wechat api"""

        cache = self._load_cache()
        token = cache.get('access_token')
        # check expires time and update token from cache
        # do a little hack
        if token and token.get('access_token') != self._WechatBasic__access_token\
                and not self._cache_expired(token):
            log.debug('get access_token from cache')
            self._WechatBasic__access_token = token.get('access_token')
            self._WechatBasic__access_token_expires_at = token.get('expires_at')
        else: # update token from wechat api
            log.debug('get access_token from offical api')
            token = super(Wechat, self).grant_token(override)
            self._update_cache(token)
        return token

    def grant_jsapi_ticket(self, override=True):
        """grant ticket from cache first, then from wechat api"""

        cache = self._load_cache()
        ticket = cache.get('jsapi_ticket')
        # check expires time and update token from cache
        # do a little hack
        if ticket and ticket.get('ticket') != self._WechatBasic__jsapi_ticket\
                and not self._cache_expired(ticket):
            log.debug('get jsapi_ticket from cache')
            self._WechatBasic__jsapi_ticket = ticket.get('ticket')
            self._WechatBasic__jsapi_ticket_expires_at = ticket.get('expires_at')
        else: # update ticket from wechat api
            log.debug('get jsapi_ticket from offical api')
            ticket = super(Wechat, self).grant_jsapi_ticket(override)
            self._update_cache(ticket)
        return ticket


# test
if __name__ == '__main__':
    a = Wechat()
    print(a.access_token)
