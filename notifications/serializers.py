#!/usr/bin/env python
# coding=utf-8
"""

__created__ = '23/3/2016'
__author__ = 'deling.ma'
"""
from rest_framework import serializers

from .models import Notification


class NotificationListSerializer(serializers.ModelSerializer):
    description = serializers.CharField(source='get_description')
    action_type = serializers.CharField(source="get_action_content_type")
    extra = serializers.JSONField(source="get_extra_data")

    class Meta:
        model = Notification
        fields = ("id", "level", "title", "description", "show_time",
                  "unread", "target",
                  "action_type", "action_object_id", "extra")
