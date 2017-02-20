# -*- coding: utf-8 -*-
from __future__ import division, unicode_literals
from dateutil import rrule

from django.db import models
from django.core.urlresolvers import reverse
from django.template.defaultfilters import date
from django.utils.translation import ugettext, ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible
from django.conf import settings

from gym.models import Gymnasium
from schedule.models.rules import Rule
from schedule.models.calendars import Calendar


class PurchaseCourse(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    gym = models.ForeignKey(Gymnasium, blank=True)
    amount = models.IntegerField("课程总量", default=0)
    remain = models.IntegerField("剩余课程", default=0)
    ctime = models.DateTimeField(auto_now_add=True)
    utime = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = "purchase_course"
        unique_together = ("user", "gym")
        verbose_name = "已购课程"
        verbose_name_plural = "已购课程"


STATE_CHOICES = (
    (-1, "休息"),
    (0, "上课"),
    (1, "结课"),
    (2, "预约"),
)


@python_2_unicode_compatible
class Event(models.Model):
    """
    This model stores meta data for a date.  You can relate this data to many
    other models.
    """
    start = models.DateTimeField(_("start"), db_index=True)
    end = models.DateTimeField(_("end"), help_text=_(
        "The end time must be later than the start time."))
    description = models.TextField(_("description"), null=True, blank=True)
    coach = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True,
                              verbose_name=_("coach"),
                              help_text=_("As coach"),
                              related_name='coach_user')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True,
                             verbose_name=_("user"),
                             help_text=_("As member"),
                             related_name='member_user')
    remind = models.IntegerField("提醒时间", default=0,
                                 help_text="事件发生前提醒；0不提醒，其他的可以写具体分钟数")
    state = models.SmallIntegerField("课程状态", default=0, choices=STATE_CHOICES)
    ctime = models.DateTimeField(_("created on"), auto_now_add=True)
    utime = models.DateTimeField(_("updated on"), auto_now=True)
    rule = models.ForeignKey(Rule, null=True, blank=True,
                             verbose_name=_("rule"),
                             help_text=_(
                                 "Select '----' for a one time only event."))
    end_recurring_period = models.DateField(
        _("end recurring period"),
        null=True, blank=True,
        help_text=_("This date is ignored for one time only events."))
    times = models.SmallIntegerField("重复次数", default=0,
                                     help_text="重复次数，当事件出现重复时需要上传")
    custom = models.CharField("自定制规则", max_length=500, blank=True, null=True,
                              help_text="星期间隔，MO, TU, WE, TH, FR, SA, SU")
    calendar = models.ForeignKey(Calendar, null=True, blank=True,
                                 verbose_name=_("calendar"))
    color_event = models.CharField(_("Color event"), null=True, blank=True,
                                   max_length=10)
    
    class Meta(object):
        verbose_name = _('event')
        verbose_name_plural = _('events')
        app_label = 'schedule'
        index_together = (("coach", "start", "end", "calendar"),
                          ("coach", "start", "end"))
        ordering = ("-start", )
    
    def __str__(self):
        return ugettext('ID:%(id)s - %(user_id)s: %(start)s - %(end)s') % {
            'id': self.id,
            'user_id': self.user_id,
            'start': date(self.start, settings.DATE_FORMAT),
            'end': date(self.end, settings.DATE_FORMAT),
        }
    
    def get_calendar_slug(self):
        return self.calendar.slug
    
    def get_color_event(self):
        state_color_config = {0: "#eddecb", 1: "#ccd5f6", 2: "#dcf5ce", -1: "#fafbfc"}
        return state_color_config.get(self.state, "#d9cbee")
    
    def get_user_info(self):
        if not self.user:
            return {}
        return {"user_id": self.user_id,
                "nickname": self.user.profile.nickname,
                "portrait": self.user.profile.portrait_url
                }
    
    def get_coach_info(self):
        if not self.coach:
            return {}
        return {"user_id": self.coach_id,
                "nickname": self.coach.profile.nickname,
                "portrait": self.coach.profile.portrait_url
                }
    
    @property
    def seconds(self):
        return (self.end - self.start).total_seconds()
    
    @property
    def minutes(self):
        return float(self.seconds) / 60
    
    @property
    def hours(self):
        return float(self.seconds) / 3600
    
    def get_absolute_url(self):
        return reverse('event', args=[self.id])
    
    def get_rrule_object(self):
        if self.rule is not None:
            params = self.rule.get_params()
            frequency = self.rule.rrule_frequency()
            return rrule.rrule(frequency, dtstart=self.start, **params)
