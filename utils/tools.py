#!/usr/bin/env python
# coding=utf-8
"""

__created__ = '13/1/2016'
__author__ = 'deling.ma'
"""
import hashlib
import datetime

from django.conf import settings


def params_filter(params):
    result = {}
    keys = params.keys()
    for key in keys:
        value = params[key]
        if value is None or value == '' or key.lower() == 'sign':
            pass
        else:
            result[key] = value
    return result


def build_sign(params):
    pre_str = ''
    params = params_filter(params)
    keys = sorted(params)
    for key in keys:
        value = params[key]
        pre_str += '%s%s' % (key, value)
    total_str = settings.ALIDAYU_APP_SECRET + pre_str + settings.ALIDAYU_APP_SECRET
    sign = hashlib.md5(total_str.encode('utf-8')).hexdigest().upper()
    return sign


def seconds_until_midnight():
    tomorrow = datetime.date.today() + datetime.timedelta(1)
    midnight = datetime.datetime.combine(tomorrow, datetime.time())
    now = datetime.datetime.now()
    return (midnight - now).seconds
