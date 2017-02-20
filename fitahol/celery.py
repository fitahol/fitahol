#!/usr/bin/env python
# coding=utf-8
"""

__created__ = '18/10/2016'
__author__ = 'deling.ma'
"""
from __future__ import absolute_import

import os
from datetime import timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fitahol.settings')

from django.conf import settings  # noqa
from celery import Celery  # noqa

# from datetime import timedelta
# from celery.schedules import crontab

app = Celery('fitahol')

app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
app.conf.update(
    CELERY_RESULT_BACKEND='djcelery.backends.database:DatabaseBackend',
)
app.conf.update(
    CELERY_TIMEZONE='Asia/Shanghai',
    CELERYBEAT_SCHEDULE={
        'del_pass_event': {
            'task': 'schedule.tasks.handle_pass_event',
            # 'schedule': crontab(hour=16, minute=5),
            'schedule': timedelta(seconds=60),
        }
    },
    # DEBUG=False
)