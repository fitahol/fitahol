#!/usr/bin/env python
# coding=utf-8
"""

__created__ = '31/1/2016'
__author__ = 'deling.ma'
"""
from rest_framework import serializers

from schedule.models import Event, Calendar, Rule, PurchaseCourse


class PurchaseCourseSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(source="user.id")
    
    class Meta:
        model = PurchaseCourse
        fields = ("id", "user_id", "amount", "remain", "gym")
        

class CalendarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Calendar


class RuleSerializer(serializers.ModelSerializer):
    params = serializers.JSONField(source='get_params')

    class Meta:
        model = Rule


class EventSerializer(serializers.ModelSerializer):
    user = serializers.JSONField(source="get_user_info")
    color_event = serializers.CharField(source="get_color_event")
    calendar_slug = serializers.CharField(source="get_calendar_slug")

    class Meta:
        model = Event
        fields = ("id", "start", "end", "user", "color_event", "custom",
                  "state", "ctime", "calendar_slug")


class CoachEventSerializer(serializers.ModelSerializer):
    user = serializers.JSONField(source="get_coach_info")
    color_event = serializers.CharField(source="get_color_event")

    class Meta:
        model = Event
        fields = ("id", "start", "end", "user", "color_event", "custom",
                  "state", "ctime")


class EventCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Event
        exclude = ("ctime", "utime")
