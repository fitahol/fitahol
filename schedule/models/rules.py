# coding=utf-8
from __future__ import unicode_literals
from django.utils.six import with_metaclass
from dateutil.rrule import DAILY, MONTHLY, WEEKLY, YEARLY, HOURLY, MINUTELY, SECONDLY
import json

from django.db import models
from django.db.models.base import ModelBase
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible

from schedule.utils import get_model_bases

freqs = (("YEARLY", _("Yearly")),
         ("MONTHLY", _("Monthly")),
         ("WEEKLY", _("Weekly")),
         ("DAILY", _("Daily")),
         ("HOURLY", _("Hourly")),
         # ("MINUTELY", _("Minutely")),
         # ("SECONDLY", _("Secondly"))
         )


@python_2_unicode_compatible
class Rule(with_metaclass(ModelBase, *get_model_bases())):
    """
    This defines a rule by which an event will recur.  This is defined by the
    rrule in the dateutil documentation.

    * name - the human friendly name of this kind of recursion.
    * description - a short description describing this type of recursion.
    * frequency - the base recurrence period
    * param - extra params required to define this type of recursion. The params
      should follow this format:

        param = [rruleparam:value;]*
        rruleparam = see list below
        value = int[,int]*

      The options are: (documentation for these can be found at
      https://dateutil.readthedocs.io/en/stable/rrule.html)
        ** count 重复次数，如指定到期时间，可无
        ** bymonth: MO, TU, WE, TH, FR, SA, SU 指定星期, 数字指定日期；
        ** bymonthday 每月日期，数字指定日期；
        ** byweekday: MO, TU, WE, TH, FR, SA, SU
        # ** bysetpos
        # ** byyearday 每年日期，数字指定天数，暂停使用；
        # ** byweekno 数字 0至6表示周一到周末；暂停使用
        # ** byhour
        # ** byminute
        # ** bysecond
        # ** byeaster
    """
    name = models.CharField(_("name"), max_length=32)
    description = models.TextField(_("description"))
    frequency = models.CharField(_("frequency"), choices=freqs, max_length=10)
    params = models.TextField(_("params"), null=True, blank=True)
    is_public = models.BooleanField("is public", default=False)

    class Meta(object):
        verbose_name = _('rule')
        verbose_name_plural = _('rules')
        app_label = 'schedule'

    def rrule_frequency(self):
        compatibiliy_dict = {
                'DAILY': DAILY,
                'MONTHLY': MONTHLY,
                'WEEKLY': WEEKLY,
                'YEARLY': YEARLY,
                'HOURLY': HOURLY,
                # 'MINUTELY': MINUTELY,
                # 'SECONDLY': SECONDLY
                }
        return compatibiliy_dict[self.frequency]

    def get_params(self):
        """
        {'count': 5, 'byweekday': [MO, TU, WE, TH]}
        """
        if self.params is None:
            return {}
        return json.loads(self.params)

    def __str__(self):
        """Human readable string for Rule"""
        return 'Rule %s params %s' % (self.name, self.params)
