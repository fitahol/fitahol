#!/usr/bin/env python
# coding=utf-8
"""

__created__ = '10/11/2016'
__author__ = 'deling.ma'
"""
from django.conf.urls import url

from wechat import views

urlpatterns = [
    url(r'^wx/$', views.WechatLoginView.as_view(), name="reset_pwd"),
]