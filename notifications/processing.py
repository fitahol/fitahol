#!/usr/bin/env python
# coding=utf-8
"""

__created__ = '01/12/2016'
__author__ = 'deling.ma'
"""
from notifications.models import Notification


def get_unread_num(user_id):
    return Notification.objects.filter(
        recipient_id=user_id, unread=True).count()