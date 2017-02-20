# coding=utf-8
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone

from django.contrib.contenttypes.fields import GenericForeignKey

from django.db import models
from django.core.exceptions import ImproperlyConfigured
from django.utils.six import python_2_unicode_compatible

from .signals import notify

from jsonfield.fields import JSONField

from django.contrib.auth.models import Group


# SOFT_DELETE = getattr(settings, 'NOTIFICATIONS_SOFT_DELETE', False)
def is_soft_delete():
    return getattr(settings, 'NOTIFICATIONS_SOFT_DELETE', False)


def assert_soft_delete():
    if not is_soft_delete():
        msg = """To use 'deleted' field, please set 'NOTIFICATIONS_SOFT_DELETE'=True in settings.
        Otherwise NotificationQuerySet.unread and NotificationQuerySet.read do NOT filter by 'deleted' field.
        """
        raise ImproperlyConfigured(msg)


class NotificationQuerySet(models.query.QuerySet):
    def unread(self):
        """Return only unread items in the current queryset"""
        if is_soft_delete():
            return self.filter(unread=True, deleted=False)
        else:
            """ when SOFT_DELETE=False, developers are supposed NOT to touch 'deleted' field.
            In this case, to improve query performance, don't filter by 'deleted' field
            """
            return self.filter(unread=True)

    def read(self):
        """Return only read items in the current queryset"""
        if is_soft_delete():
            return self.filter(unread=False, deleted=False)
        else:
            """ when SOFT_DELETE=False, developers are supposed NOT to touch 'deleted' field.
            In this case, to improve query performance, don't filter by 'deleted' field
            """
            return self.filter(unread=False)

    def mark_all_as_read(self, recipient=None):
        """Mark as read any unread messages in the current queryset.

        Optionally, filter these by recipient first.
        """
        # We want to filter out read ones, as later we will store
        # the time they were marked as read.
        qs = self.unread()
        if recipient:
            qs = qs.filter(recipient=recipient)

        qs.update(unread=False)

    def mark_all_as_unread(self, recipient=None):
        """Mark as unread any read messages in the current queryset.

        Optionally, filter these by recipient first.
        """
        qs = self.read()

        if recipient:
            qs = qs.filter(recipient=recipient)

        qs.update(unread=True)

    def deleted(self):
        """Return only deleted items in the current queryset"""
        assert_soft_delete()
        return self.filter(deleted=True)

    def active(self):
        """Return only active(un-deleted) items in the current queryset"""
        assert_soft_delete()
        return self.filter(deleted=False)

    def mark_all_as_deleted(self, recipient=None):
        """Mark current queryset as deleted.
        Optionally, filter by recipient first.
        """
        assert_soft_delete()
        qs = self.active()
        if recipient:
            qs = qs.filter(recipient=recipient)

        qs.update(deleted=True)

    def mark_all_as_active(self, recipient=None):
        """Mark current queryset as active(un-deleted).
        Optionally, filter by recipient first.
        """
        assert_soft_delete()
        qs = self.deleted()
        if recipient:
            qs = qs.filter(recipient=recipient)

        qs.update(deleted=False)

LEVELS = (
    (0, '通知'),
    (1, '私信'),
    (2, '评论'),
    (3, '@我'),
)


@python_2_unicode_compatible
class Notification(models.Model):
    level = models.IntegerField("推送类型", choices=LEVELS, default=0)
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True,
                               related_name="sender_notify")
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL,
                                  related_name='recipient_notify')

    target = models.CharField("跳转类型", max_length=500, default="html",
                              help_text="空为不跳转, html为跳网页, app为跳转数据页")
    title = models.CharField("标题", max_length=200, blank=True)
    description = models.TextField(blank=True, null=True)
    action_object_content_type = models.ForeignKey(
        ContentType, blank=True, null=True, related_name='notify_action_object')
    action_object_id = models.CharField(max_length=255, blank=True,
                                        null=True)
    action_object = GenericForeignKey('action_object_content_type',
                                      'action_object_id')
    show_time = models.DateTimeField(u"展示时间", db_index=True)

    unread = models.BooleanField(default=True, blank=False)
    deleted = models.BooleanField(default=False)
    notified = models.BooleanField(default=False)

    data = JSONField(blank=True, null=True,
                     help_text="定制信息, 默认为空; 网页跳转写 {'target_url': ''}")
    objects = NotificationQuerySet.as_manager()

    ctime = models.DateTimeField(u"创建时间", auto_now_add=True)
    utime = models.DateTimeField(u"更新时间", auto_now=True)

    class Meta:
        ordering = ('-ctime',)
        app_label = 'notifications'
        verbose_name = "站内信通知"
        verbose_name_plural = "站内信通知"

    def __str__(self):
        ctx = {
            'action_object': self.action_object,
            'target': self.target,
            'timesince': self.timesince()
        }
        if self.action_object:
            return u'%(action_object)s ~ %(timesince)s 之前' % ctx
        return u' %(timesince)s之前' % ctx

    def timesince(self, now=None):
        """
        Shortcut for the ``django.utils.timesince.timesince`` function of the
        current timestamp.
        """
        from django.utils.timesince import timesince as timesince_
        return timesince_(self.ctime, now)

    def get_description(self):
        if self.description:
            return self.description
        return self.__str__()

    def get_action_content_type(self):
        return self.action_object_content_type.model

    def get_extra_data(self):
        if not self.data:
            return {}
        return self.data

    def mark_as_read(self):
        if self.unread:
            self.unread = False
            self.save()

    def mark_as_unread(self):
        if not self.unread:
            self.unread = True
            self.save()


def notify_handler(**kwargs):
    """
    Handler function to create Notification instance upon action signal call.
    """
    kwargs.pop('signal', None)
    recipient = kwargs.pop('recipient')
    sender = kwargs.pop('sender')
    description = kwargs.pop('description', '')
    title = kwargs.pop('title', '')
    target = kwargs.pop('target', '')
    show_time = kwargs.pop('show_time', timezone.now())
    action_object = kwargs.pop('action_object')
    level = kwargs.pop('level', 0)

    # Check if User or Group
    if isinstance(recipient, Group):
        recipients = recipient.user_set.all()
    else:
        recipients = [recipient]

    for recipient in recipients:
        new_notify = Notification(
            recipient=recipient,
            sender=sender,
            action_object_content_type=ContentType.objects.get_for_model(action_object),
            action_object_id=action_object.pk,
            title=title,
            description=description,
            target=target,
            show_time=show_time,
            level=level
        )

        # # Set optional objects
        # for obj, opt in optional_objs:
        #     if obj is not None:
        #         setattr(newnotify, '%s_object_id' % opt, obj.pk)
        #         setattr(newnotify, '%s_content_type' % opt,
        #                 ContentType.objects.get_for_model(obj))

        if len(kwargs):
            new_notify.data = kwargs
        new_notify.save()


# connect the signal
notify.connect(notify_handler, dispatch_uid=None)
