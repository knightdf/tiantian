# coding=utf-8

Testing = False

################### Server Config ###################
RedisUrl = None # "/tmp/redis.sock"
RedisAddr = "127.0.0.1"
RedisPort = "6379"

MySqlHost = "127.0.0.1"
MySqlPort = "3306"
MySqlUser = "ray"
MySqlPass = ""
MySqlDB = "wechat_tiantian"


################### App Config ###################
Token = ""
EncodingAESKey = ""
AppID = ""
AppSecret = ""

# Turing Robot
TuringRobotKey = "3b41482640b3ababc622e7ff71da5c9e"

################### Logging Config ###################
LogPath = "/yundisk/log/wechat/wechat.log"
LogLevel = "DEBUG"

# mail notification for CRITICAL error message
MailNotifyEnable = True
MailHost = "smtp.mxhichina.com"
MailFrom = "wechat@irayd.com"
MailTo = "lei310@163.com"
MailPass = ""


################### Testing Config ###################
if Testing:
    Token = "spamtest"
    EncodingAESKey = "abcdefghijklmnopqrstuvwxyz0123456789ABCDEFG"
    AppID = "wx1641680a4b30b343"
    AppSecret = "d4624c36b6795d1d99dcf0547af5443d"
