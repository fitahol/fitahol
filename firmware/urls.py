#!/usr/bin/env python
# coding=utf-8
"""

__created__ = '1/1/2016'
__author__ = 'deling.ma'
"""
from django.conf.urls import url

from firmware import views

urlpatterns = [
    url(r'^valid_code/$', views.ValidCodeView.as_view(), name="valid_code"),
    url(r'feedback/add/$', views.FeedbackView.as_view(), name='feedback-add'),
    url(r'feedback/$', views.FeedbackViewSet.as_view(), name='feedback'),
    url(r'(?P<platform>\w{0,10})/upgrade/$', views.ClientVersionView.as_view(),
        name='client_upgrade'),
]
