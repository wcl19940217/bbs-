# 密码存储要使用的
import os
import random


SECRET_KEY = os.urandom(24)

# debug模式
DEBUG = True

# 数据库连接
DB_USERNAME = 'wang'
DB_PASSWORD = 'wang'
DB_HOST = '127.0.0.1'
DB_PORT = '3306'
DB_NAME = 'cms_lt'

DB_URI = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'.format(DB_USERNAME, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME)

SQLALCHEMY_DATABASE_URI = DB_URI
SQLALCHEMY_TRACK_MODIFICATIONS = False


# session
CMS_USER_ID = ''
FRONT_USER_ID = ''


# MAIL_USE_TLS：端口号587
# MAIL_USE_SSL：端口号465
# QQ邮箱不支持非加密方式发送邮件
# 发送者邮箱的服务器地址
MAIL_SERVER = "smtp.qq.com"
MAIL_PORT = '587'
MAIL_USE_TLS = True
# MAIL_USE_SSL
MAIL_USERNAME = "******@qq.com"
MAIL_PASSWORD = ""  # 不是QQ密码是邮箱里面一个密码
MAIL_DEFAULT_SENDER = "*******@qq.com"


# 短信验证码
Text_model = "您的验证码是：{}{}{}{}。请不要把验证码泄露给其他人。".format(random.randint(0, 10), random.randint(0, 10), random.randint(0, 10),
                                                   random.randint(0, 10))


# flask_page
PER_PAGE = 10