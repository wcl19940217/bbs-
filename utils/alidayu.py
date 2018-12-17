# 接口类型：互亿无线触发短信接口，支持发送验证码短信、订单通知短信等。
# 账户注册：请通过该地址开通账户http://user.ihuyi.com/register.html
# 注意事项：
# （1）调试期间，请使用用系统默认的短信内容：您的验证码是：【变量】。请不要把验证码泄露给其他人。
# （2）请使用 APIID 及 APIKEY来调用接口，可在会员中心获取；
# （3）该代码仅供接入互亿无线短信接口参考使用，客户可根据实际需要自行编写；

# !/usr/local/bin/python
# -*- coding:utf-8 -*-
# import httplib   #python2.版本里面的
import http.client
from urllib import parse
import random


host = "106.ihuyi.com"
sms_send_uri = "/webservice/sms.php?method=Submit"

# 自己去https://user.ihuyi.com/注册使用
# 查看用户名 登录用户中心->验证码通知短信>产品总览->API接口信息->APIID
account = "*****"
# 查看密码 登录用户中心->验证码通知短信>产品总览->API接口信息->APIKEY
password = "*****"
#


def send_sms(text, mobile):
    params = parse.urlencode(
        {'account': account, 'password': password, 'content': text, 'mobile': mobile, 'format': 'json'})
    headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
    conn = http.client.HTTPConnection(host, port=80, timeout=30)
    conn.request("POST", sms_send_uri, params, headers)
    response = conn.getresponse()
    response_str = response.read()
    conn.close()
    return response_str


# if __name__ == '__main__':
#     mobile = "176******"
#     text = "您的验证码是：{}{}{}{}。请不要把验证码泄露给其他人。".format(random.randint(0,10),random.randint(0,10),random.randint(0,10),
#                                                    random.randint(0, 10))
#     # print(send_sms(text, mobile))
#
#     s = text[7:11]

# while True:
#     cmd = input('>>>>')
#     if cmd.strip() == s:
#         print('good')
#         break
#     else:
#         print('请重新输入')