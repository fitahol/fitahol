# -*- coding: utf-8 -*-

from django.contrib import admin
from .models import Notification


class NotificationAdmin(admin.ModelAdmin):
    list_display = ('id', 'recipient', 'level', 'target', 'unread')
    list_filter = ('level', 'unread', 'ctime', )

admin.site.register(Notification, NotificationAdmin)
