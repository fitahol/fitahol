# -*- coding: utf-8 -*-

from django.conf.urls import url

from . import views

app_name = 'notifications'

urlpatterns = [
    url(r'^$', views.AllNotificationsList.as_view(), name='all'),
    url(r'^unread/$', views.UnreadNotificationsList.as_view(), name='unread'),
    url(r'^mark_all_read/$', views.MarkAllAsRead, name='mark_all_as_read'),
    url(r'^mark_read/(?P<pk>\d+)/$', views.MarkAsRead, name='mark_as_read'),
    url(r'^mark_unread/(?P<pk>\d+)/$', views.MarkAsUnread,
        name='mark_as_unread'),
    url(r'^(?P<pk>\d+)/$', views.NotificationView.as_view(),
        name='notification_detail'),
    url(r'^unread_count/$', views.UnreadCountView,
        name='unread_notification_count'),
]
