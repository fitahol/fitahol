#!/usr/bin/env python
# coding=utf-8
"""

__created__ = '31/1/2016'
__author__ = 'deling.ma'
"""
from rest_framework import routers
from django.conf.urls import url

from gym import views

router = routers.DefaultRouter()
router.register(r'gym', views.GymnasiumViewSet)

urlpatterns = [
    url(r'^province/$', views.ProvinceListView.as_view(),
        name="province_list"),
    url(r'^city/(?P<pcode>[0-9]+)/$', views.CityListView.as_view(),
        name="city_list"),
    url(r'^district/(?P<pcode>[0-9]+)/$', views.DistrictListView.as_view(),
        name="district_list"),
]

urlpatterns += router.urls
