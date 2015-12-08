#!/usr/bin/python
# coding=utf-8

import redis
import MySQLdb
import config

# default values
DEFAULT_REDIS_IP = '127.0.0.1'
DEFAULT_REDIS_PORT = 6379

DEFAULT_MYSQL_IP = '127.0.0.1'
DEFAULT_MYSQL_PORT = 3306

class RedisCache(object):
    """
    cache a connection pool in process(Class) but not in one Redis instance
    """

    @staticmethod
    def create_pool():
        redis_url = config.RedisUrl
        redis_ip = config.RedisAddr or DEFAULT_REDIS_IP
        redis_port = config.RedisPort or DEFAULT_REDIS_PORT

        # REDIS_URL takes precedence over host/port specification
        if redis_url:
            RedisCache.pool = redis.ConnectionPool().from_url(redis_url)
        else:
            RedisCache.pool = redis.ConnectionPool(host = redis_ip, port = redis_port)

    def __init__(self):
        if not hasattr(RedisCache, 'pool'):
            RedisCache.create_pool()
        self._conn = redis.Redis(connection_pool = RedisCache.pool)

    # get redis instance
    def get_connection(self):
        return self._conn

class MysqlCache(object):
    """
    cache a mysql connection pool
    """
    def __init__(self):
        db_host = config.MySqlHost or DEFAULT_MYSQL_IP
        db_port = config.MySqlPort or DEFAULT_MYSQL_PORT
        db_user = config.MySqlUser or 'root'
        db_passwd = config.MySqlPass or None
        db_name = config.MySqlDB or None
        assert db_name is not None, 'No database specified in settings'

        self._conn = MySQLdb.connect(host = db_host, user = db_user,\
                passwd = db_passwd, db = db_name, port = db_port)

    def get_connection(self):
        return self._conn
