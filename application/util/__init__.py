# coding=utf-8

import requests
import json

def _request(method, url, **kwargs):
    """
    For json based request and response only.
    perform http request, use params to set uri args, data to set post body data.
        get: _request('get', url, params={x: x, y: y})
        post: _request('post', url, data={name: value})
    """

    # encode unicode with utf-8
    if 'params' in kwargs:
        for key in kwargs.get('params').iterkeys():
            value = kwargs['params'][key]
            if isinstance(value, unicode):
                kwargs['params'][key] = value.encode('utf-8')

    if isinstance(kwargs.get('data', ''), dict):
        body = json.dumps(kwargs['data'], ensure_ascii=False)
        body = body.encode('utf8')
        kwargs['data'] = body

    r = requests.request(
        method=method,
        url=url,
        **kwargs
    )
    r.raise_for_status()
    response_json = r.json()
    return response_json

def get(url, **kwargs):
    return _request('get', url, **kwargs)

def post(url, **kwargs):
    return _request('post', url, **kwargs)

def transcoding(data):
    """
    transform encoding for list, decode to unicode
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

def transcoding_list(data):
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
            result.append(transcoding_dict(item))
        elif isinstance(item, list):
            result.append(transcoding_list(item))
        else:
            result.append(transcoding(item))
    return result

def transcoding_dict(data):
    """
    transform encoding for dict, decode to unicode
    :param data: dict
    :return: dict
    """
    if not isinstance(data, dict):
        raise ValueError('Parameter data must be dict object.')

    result = {}
    for k, v in data.items():
        k = transcoding(k)
        if isinstance(v, dict):
            v = transcoding_dict(v)
        elif isinstance(v, list):
            v = transcoding_list(v)
        else:
            v = transcoding(v)
        result.update({k: v})
    return result


# test
if __name__ == '__main__':
    print(get('http://www.tuling123.com/openapi/api', params={'key': '3b41482640b3ababc622e7ff71da5c9e', 'info': u'你好', 'loc': None}))
