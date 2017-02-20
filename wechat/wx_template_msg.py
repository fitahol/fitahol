#!/usr/bin/env python
# coding=utf-8
"""

__created__ = '30/11/2016'
__author__ = 'deling.ma'
"""
from django.conf import settings

from .sdk.basic import WechatBasic
from account.models import Profile


def get_wechat_conn(profile):
    if profile.u_type == 1:
        wechat = WechatBasic(token=settings.WECHAT_TOKEN,
                             appid=settings.WECHAT_APP_ID,
                             appsecret=settings.WECHAT_APP_SECRET)
    else:
        wechat = WechatBasic(token=settings.WECHAT_TOKEN,
                             appid=settings.WECHAT_MEMBER_APP_ID,
                             appsecret=settings.WECHAT_MEMBER_APP_SECRET)
    return wechat


def send_member_add_msg(user_id, form_id):
    """审核通知"""
    template_id = "aH2UF5VbtWWD73Oioc-zJ5wFa4H1CcHbydw5TKqfhgo"
    data = {"keyword1": "学员名", "keyword2": "添加学员", "状态": "请求添加", "备注": ""}
    page = "/pages/addMember/add?user_id=%s" % user_id
    profile_obj = Profile.objects.get(user_id=user_id)
    try:
        openid = profile_obj.user.wechatinfo.openid
    except Exception:
        return
    wechat = get_wechat_conn(profile_obj)
    wechat.send_wx_template_message(openid, form_id, template_id, data, page)
    return


def send_coach_add_msg(user_id, ):
    """审核通知"""
    wechat = get_wechat_conn()
    wechat.send_wx_template_message()
    return


def send_course_booking_msg(user_id, ):
    """开课提醒"""
    wechat = get_wechat_conn()
    wechat.send_wx_template_message()
    return


def send_booking_success_msg(user_id, ):
    """课程预约成功提醒"""
    wechat = get_wechat_conn()
    wechat.send_wx_template_message()
    return


def send_booking_failed_msg(user_id, ):
    """报名失败通知"""
    wechat = get_wechat_conn()
    wechat.send_wx_template_message()
    return
