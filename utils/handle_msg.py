#!/usr/bin/env python
# coding=utf-8
"""

__created__ = '13/1/2016'
__author__ = 'deling.ma'
"""
import time
import requests
from django.conf import settings
from django.core.mail import EmailMultiAlternatives

from utils.tools import build_sign

sms_base_params = {
    "app_key": settings.ALIDAYU_APP_ID,
    "method": "alibaba.aliqin.fc.sms.num.send",
    "sign_method": "md5",
    "format": "json",
    "v": "2.0",
}


def send_register_sms(v_code, account):
    register_params = {"sms_type": "normal",
                       "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                       "sms_free_sign_name": "注册验证",
                       "sms_param": '{"code": "%s", "product": "Fitahol"}' % v_code,
                       "rec_num": account,
                       "sms_template_code": "SMS_25270213"}
    sms_base_params.update(register_params)
    return send_alidayu_sms(sms_base_params)


def send_auth_valid_sms(v_code, account):
    register_params = {"sms_type": "normal",
                       "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                       "sms_free_sign_name": "身份验证",
                       "sms_param": '{"code": "%s", "product": "Fitahol"}' % v_code,
                       "rec_num": account,
                       "sms_template_code": "SMS_25055166"}
    sms_base_params.update(register_params)
    return send_alidayu_sms(sms_base_params)


def send_alidayu_sms(params):
    url = "http://gw.api.taobao.com/router/rest"
    sign = build_sign(params)
    params.update({"sign": sign})
    response = requests.post(url, data=params)
    if response.status_code == 200:
        result = response.json()
        if result["alibaba_aliqin_fc_sms_num_send_response"]["result"][
                "err_code"] == 0:
            return True
    return False


valid_code_content = """
  <p>您的验证码为: {valid_code}
      <dl>
        <dt>验证码3分钟后失效, 请及时使用.</dd>
        <dt>请勿将验证码发给其他人, 管理员不会向您索取验证码. </dd>
      </dl>
  </p>
"""


def send_email_msg(subject, content, rcp_list, from_email=None):
    if not from_email:
        from_email = settings.DEFAULT_FROM_EMAIL
    text_content = content
    html_content = '<div>%s</div>' % content
    if not isinstance(rcp_list, list):
        rcp_list = [rcp_list, ]
    msg = EmailMultiAlternatives(subject, text_content, from_email, rcp_list)
    msg.attach_alternative(html_content, "text/html")
    msg.send()
