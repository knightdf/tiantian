# coding=utf-8

import requests
import json


def get(url, params=None, **kwargs):
    """
    For json based request and response only.
    :param params: bytes or dict pass to uri args
    :return: dict
    """

    if params:
        if isinstance(params, basestring):
            params = encode(params)
        elif isinstance(params, dict):
            params = encode_dict(params)
        else:
            raise ValueError('Get params can only be dictionary or bytes')

    r = requests.get(url, params, **kwargs)
    r.raise_for_status()
    return r.json()

def post(url, data=None, **kwargs):
    """
    For json based request and response only.
    :param data: bytes, dict or file-like object post to url
    :return: dict
    """

    if data:
        if isinstance(data, basestring):
            params = encode(data)
        elif isinstance(data, dict):
            params = encode_dict(data)
        elif isinstance(data, file):
            pass
        else:
            raise ValueError('Post data can only be dictionary or bytes or file-like object')

    r = requests.post(url, data, **kwargs)
    r.raise_for_status()
    return r.json()

def encode(data):
    """
    encode in utf-8
    :param data: unicode
    :return: str
    """

    if not data:
        return data
    result = None
    if isinstance(data, unicode):
        result = data.encode('utf-8')
    else:
        result = data
    return data

def encode_list(data):
    """
    transform encoding for list, encode in utf-8
    :param data: list
    :return: list
    """
    if not isinstance(data, list):
        raise ValueError('Parameter data must be list object.')

    result = []
    for item in data:
        if isinstance(item, dict):
            result.append(encode_dict(item))
        elif isinstance(item, list):
            result.append(encode_list(item))
        else:
            result.append(encode(item))
    return result

def encode_dict(data):
    """
    transform encoding for dict, encode in utf-8
    :param data: dict
    :return: dict
    """
    if not isinstance(data, dict):
        raise ValueError('Parameter data must be dict object.')

    result = {}
    for k, v in data.items():
        k = encode(k)
        if isinstance(v, dict):
            v = encode_dict(v)
        elif isinstance(v, list):
            v = encode_list(v)
        else:
            v = encode(v)
        result.update({k: v})
    return result

def decode(data):
    """
    decode to unicode
    :param data: str
    :return: unicode
    """
    if not data:
        return data

    result = None
    if isinstance(data, str):
        result = data.decode('utf-8')
    else:
        result = data
    return result

def decode_list(data):
    """
    transform encoding for list, decode to unicode
    :param data: list
    :return: list
    """
    if not isinstance(data, list):
        raise ValueError('Parameter data must be list object.')

    result = []
    for item in data:
        if isinstance(item, dict):
            result.append(decode_dict(item))
        elif isinstance(item, list):
            result.append(decode_list(item))
        else:
            result.append(decode(item))
    return result

def decode_dict(data):
    """
    transform encoding for dict, decode to unicode
    :param data: dict
    :return: dict
    """
    if not isinstance(data, dict):
        raise ValueError('Parameter data must be dict object.')

    result = {}
    for k, v in data.items():
        k = decode(k)
        if isinstance(v, dict):
            v = decode_dict(v)
        elif isinstance(v, list):
            v = decode_list(v)
        else:
            v = decode(v)
        result.update({k: v})
    return result


# test
if __name__ == '__main__':
    print(post('http://www.tuling123.com/openapi/api', {'key': '3b41482640b3ababc622e7ff71da5c9e', 'info': u'你好', 'loc': None}))
