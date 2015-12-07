# coding=utf-8

from wechat import Wechat
from log.logger import log
from wechat_sdk.exceptions import *
from wechat_sdk.messages import *


def create_menu(menu_data):
    wechat = Wechat()
    wechat.create_menu(menu_data)

