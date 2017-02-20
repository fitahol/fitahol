#!/usr/bin/env python
# coding=utf-8
"""

__created__ = '4/17/16'
__author__ = 'deling.ma'
"""
from django.contrib import admin

from firmware.models import Feedback


class FeedbackAdmin(admin.ModelAdmin):
    list_display = ("id", "nickname", "contact", "content")

admin.site.register(Feedback, FeedbackAdmin)

