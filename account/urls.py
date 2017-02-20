#!/usr/bin/env python
# coding=utf-8
"""

__created__ = '1/1/2016'
__author__ = 'deling.ma'
"""
from django.conf.urls import url
from rest_framework import routers

from account import views

router = routers.DefaultRouter()
router.register(r'profile', views.ProfileViewSet)
router.register(r'coach', views.CoachViewSet)
router.register(r'member', views.MemberViewSet)
router.register(r'figure', views.FigureViewSet)
# router.register(r'wechat_profile', views.WechatInfoViewSet)

urlpatterns = [
    url(r'^reset_pwd/$', views.ResetPasswordView.as_view(), name="reset_pwd"),
    url(r'^reset_phone/$', views.ResetPhoneView.as_view(), name="reset_phone"),
    url(r'^register/$', views.RegisterView.as_view(), name="register"),
    url(r'^del/relation/$', views.DelRelationView.as_view(), name="del_ref"),
    url(r'^login/$', views.LoginView.as_view(), name="login"),
    url(r'^(?P<pk>[0-9]+)/$', views.AccountView.as_view(), name="account"),
    url(r'^portrait/$', views.PortraitView.as_view(), name="portrait"),
    url(r'^relation/$', views.UserRelationView.as_view(),
        name="user_relation"),
    url(r'^relation/(?P<pk>[0-9]+)/$', views.UserRelationConfirmView.as_view(),
        name="relation_confirm"),
]

urlpatterns += router.urls
