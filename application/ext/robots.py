# coding=utf-8

from application import util
from application.log.logger import log
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


class TuringRobot(object):
    """A Turing Robot using api of tuling123.com"""

    _Error = {
            '40001': u'额，出错啦o(╯□╰)o',
            '40002': u'说点什么吧',
            '40003': u'额，出错啦o(╯□╰)o',
            '40004': u'今天太累了，要休息下了。明天再来跟我聊天吧^ ^',
            '40005': u'这个我也不知道耶...囧',
            '40006': u'我出去锻炼啦，等一下回来噢0 0',
            '40007': u'(⊙o⊙)…您说的我没听懂耶'
            }

    _Code = {
            '100000': 'text',
            '200000': 'link',
            '302000': 'news',
            '305000': 'train',
            '306000': 'flight',
            '308000': 'cookbook'
            }

    def __init__(self, key):
        self._key = key

    def answer(self, message, userid=None, location=None, longitude=None, latitude=None):
        response = util.post(
                'http://www.tuling123.com/openapi/api',
                data={
                    'key': self._key,
                    'info': message,
                    'userid': userid,
                    'loc': location,
                    'lon': longitude,
                    'lat': latitude}
                )
        err_msg = self.check_error(response)
        if err_msg:
            log.error('Turing Robot Error, code: %s, query string: %s' % (str(response.get('code')), str(msg)))
            return err_msg
        return self.plain_text(response)

    def check_error(self, resp):

        return self._Error.get(str(resp.get('code')))

    def plain_text(self, resp):
        """convert json message to plain text"""

        code = str(resp.get('code'))

        if self._Code.get(code) == 'text':
            return resp.get('text')
        elif self._Code.get(code) == 'link':
            return u"%(text)s: \n%(url)s" % resp
        elif self._Code.get(code) == 'news':
            news = []
            for item in resp.get('list', []):
                news.append(u"标题: %(article)s\n来源: %(source)s\n阅读原文: %(detailurl)s" % item)
            return u"%(text)s: \n" % resp + u'\n---\n'.join(news)
        elif self._Code.get(code) == 'train':
            trains = []
            for train in resp.get('list', []):
                trains.append(u"车次: %(trainnum)s\n出发站: %(start)s\n到达站: %(terminal)s\
                        \n开车时间: %(starttime)s\n到达时间: %(endtime)s\n详情: %(detailurl)s" % train)
            return u"%(text)s: \n" % resp + u'\n---\n'.join(trains)
        elif self._Code.get(code) == 'flight':
            flights = []
            for flight in resp.get('list', []):
                flights.append(u"航班号: %(flight)s\n起飞时间: %(starttime)s\n到达时间: %(endtime)s" % flight)
            return u"%(text)s: \n" % resp + u'\n---\n'.join(flights)
        elif self._Code.get(code) == 'cookbook':
            cookbooks = []
            for cookbook in resp.get('list', []):
                cookbooks.append(u"菜名: %(name)s\n菜谱: %(info)s\n详情: %(detailurl)s" % cookbook)
            return u"%(text)s: \n" % resp + u'\n---\n'.join(cookbooks)
        else:
            return resp.get('text')
