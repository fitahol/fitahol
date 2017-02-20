#!/usr/bin/env python
# coding=utf-8
"""

__created__ = '18/10/2016'
__author__ = 'deling.ma'
"""
import logging
import datetime
from dateutil.relativedelta import relativedelta

from celery import shared_task

from schedule.models import Event, Rule

logger = logging.getLogger("default")


@shared_task
def handle_pass_event():
    # 处理过期事件
    now = datetime.datetime.now()
    Event.objects.filter(state=0, end__lt=now, calendar__slug="default").update(state=1)


def add_new_event(instance, temp_date):
    # 处理事件
    temp_start = instance.start.replace(
        year=temp_date.year, month=temp_date.month, day=temp_date.day)
    temp_end = instance.end.replace(
        year=temp_date.year, month=temp_date.month, day=temp_date.day)
    instance.id = None
    instance.start = temp_start
    instance.end = temp_end
    instance.save()


def handle_rul_custom_week(instance):
    # "MO, TU, WE, TH, FR, SA, SU" 处理定制星期
    weekday_config = {"MO": 0, "TU": 1, "WE": 2, "TH": 3, "FR": 4, "SA": 5,
                      "SU": 6}
    weekno_custom = [weekday_config.get(weekday) for weekday in
                     instance.custom.split(",")]
    start = instance.start
    end = instance.end_recurring_period
    delta = datetime.timedelta(days=1)
    temp_date = start + delta
    count = 1
    while temp_date.date() <= end and count < instance.times:
        if temp_date.weekday() in weekno_custom:
            add_new_event(instance, temp_date)
            count += 1
        temp_date += delta


def handle_rule_month_today(instance):
    start = instance.start
    end = instance.end_recurring_period
    delta = relativedelta(month=+1)
    temp_date = start + delta
    count = 1
    while temp_date.date() <= end and count < instance.times:
        if temp_date.day == temp_date.day:
            add_new_event(instance, temp_date)
            count += 1
        temp_date += delta


def handle_rule_week_today(instance):
    start = instance.start
    end = instance.end_recurring_period
    delta = relativedelta(weeks=1)
    temp_date = start + delta
    count = 1
    while temp_date.date() <= end and count < instance.times:
        if temp_date.day == temp_date.day:
            add_new_event(instance, temp_date)
            count += 1
        temp_date += delta


def handle_rule_everyday(instance):
    start = instance.start
    end = instance.end_recurring_period
    delta = datetime.timedelta(days=1)
    temp_date = start + delta
    count = 1
    while temp_date.date() <= end and count < instance.times:
        add_new_event(instance, temp_date)
        count += 1
        temp_date += delta


@shared_task
def event_rule_task(event_id):
    logger.info("event_id: %s" % event_id)
    instance = Event.objects.get(id=event_id)
    if not instance.rule:
        return "success"
    if instance.custom:
        handle_rul_custom_week(instance)
    if instance.rule.frequency == "MONTHLY":
        handle_rule_month_today(instance)
    elif instance.rule.frequency == "WEEKLY":
        handle_rule_week_today(instance)
    elif instance.rule.frequency == "DAILY":
        handle_rule_everyday(instance)
    else:
        pass
    return event_id
