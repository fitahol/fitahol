#!/usr/bin/env python
# coding=utf-8
"""

__created__ = '31/1/2016'
__author__ = 'deling.ma'
"""
from rest_framework import serializers
from gym.models import Gymnasium, Province, City, District


class ProvinceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Province
        fields = ("code", "name", "fullname", "pinyin", "suffix")


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ("code", "name", "fullname", "pinyin", "suffix")


class DistrictSerializer(serializers.ModelSerializer):
    class Meta:
        model = District
        fields = ("code", "name", "fullname", "pinyin", "suffix")


class GymnasiumSerializer(serializers.ModelSerializer):
    city_info = serializers.JSONField(source="full_city_info")
    
    class Meta:
        model = Gymnasium
        fields = ("id", "name", "address", "telephone", "lat", "lng", "city_info")


class GymnasiumCreateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Gymnasium
        fields = ("name", "address", "telephone", "lat", "lng",
                  "city_code", "district_code")
