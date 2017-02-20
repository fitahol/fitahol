#!/usr/bin/env python
# coding=utf-8
"""

__created__ = '23/10/2016'
__author__ = 'deling.ma'
"""
from rest_framework import serializers

from .models import ClientVersion, Feedback


class ClientVersionSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ClientVersion
        fields = ("id", "url", "")


class FeedbackSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Feedback
        fields = ("nickname", "contact", "content")
