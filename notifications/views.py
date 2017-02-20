# coding=utf-8
from django.conf import settings
from django.shortcuts import get_object_or_404
from rest_framework import status

from rest_framework.generics import ListAPIView, RetrieveDestroyAPIView
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from notifications.serializers import NotificationListSerializer
from .models import Notification


class AllNotificationsList(ListAPIView):
    serializer_class = NotificationListSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        if getattr(settings, 'NOTIFICATIONS_SOFT_DELETE', False):
            qs = self.request.user.recipient_notify.active()
        else:
            qs = self.request.user.recipient_notify.all()
        return qs


class NotificationView(RetrieveDestroyAPIView):
    serializer_class = NotificationListSerializer
    queryset = Notification.objects.all()
    permission_classes = (IsAuthenticated,)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.unread = False
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        notification = get_object_or_404(
            Notification, recipient=request.user, id=kwargs["pk"])

        if getattr(settings, 'NOTIFICATIONS_SOFT_DELETE', False):
            notification.deleted = True
            notification.save()
        else:
            notification.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UnreadNotificationsList(ListAPIView):
    serializer_class = NotificationListSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = None

    def get_queryset(self):
        return self.request.user.recipient_notify.unread()


class MarkAllAsRead(APIView):
    serializer_class = NotificationListSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        request.user.recipient_notify.mark_all_as_read()
        return Response({"detail": "请求成功"})


class MarkAsRead(APIView):
    serializer_class = NotificationListSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        notification = get_object_or_404(
            Notification, recipient=request.user, id=kwargs["pk"])
        notification.mark_as_read()
        return Response({"detail": "请求成功"})


class MarkAsUnread(APIView):
    serializer_class = NotificationListSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        notification = get_object_or_404(
            Notification, recipient=request.user, id=kwargs["pk"])
        notification.mark_as_unread()
        return Response({"detail": "请求成功"})


class UnreadCountView(APIView):
    serializer_class = NotificationListSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        data = {
            'unread_count': request.user.recipient_notify.unread().count(),
        }
        return Response(data)
