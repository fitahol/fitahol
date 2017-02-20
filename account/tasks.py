#!/usr/bin/env python
# coding=utf-8
"""

__created__ = '18/10/2016'
__author__ = 'deling.ma'
"""
import logging
import datetime
import random

from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.db import IntegrityError

from account.models import CoachMemberRef
from fitness.models import FitGoal, GoalRecord, FitnessExercise, ExerciseRecord
from notifications.models import Notification
from schedule.models import Event, Calendar, PurchaseCourse

from celery import shared_task
# from celery.task import periodic_task

logger = logging.getLogger("default")


@shared_task
def init_new_user(user_id):
    # 初始化新用户信息
    calendar_obj = Calendar.objects.get(slug="default")
    # 绑定学员 健身小助手
    user_obj = get_user_model().objects.get(id=user_id)
    helper_obj = get_user_model().objects.get(username="小助手")
    if user_obj.profile.u_type == 1:
        # 如果用户是教练，添加小助手为学员
        coach_user = user_obj
        member_user = helper_obj
    else:
        coach_user = helper_obj
        member_user = user_obj
    CoachMemberRef(member=member_user.member, coach=coach_user.coach).save()
    # 创建 把课程时间&课程动作记录&健身记录 时间为本周末
    today = datetime.datetime.today()
    start = today.replace(hour=14, minute=0, second=0)
    end = today.replace(hour=15, minute=0, second=0)
    
    event_queryset = Event.objects.filter(user=member_user, start=start)
    month_ago = today - datetime.timedelta(days=30)
    Event.objects.filter(ctime__lt=month_ago).delete()
    if not event_queryset:
        new_event = Event(coach=coach_user, user=member_user, start=start, end=end,
                          description="示例数据，可删除", calendar=calendar_obj,
                          color_event="#f4f4f4")
        new_event.save()
    else:
        new_event = event_queryset[0]
    try:
        new_course = PurchaseCourse(user=member_user, amount=1, remain=1)
        new_course.save()
    except IntegrityError:
        pass
    ExerciseRecord.objects.filter(user=helper_obj).delete()
    for i in range(7):
        temp_id = random.randint(0, 340)
        try:
            exercise_obj = FitnessExercise.objects.get(id=temp_id)
            new_exc_record = ExerciseRecord(event=new_event,
                                            user=member_user,
                                            exercise=exercise_obj, value=10,
                                            number=15)
            new_exc_record.save()
        except FitnessExercise.DoesNotExist:
            pass
    lose_goal, _ = FitGoal.objects.get_or_create(
            name="健身减脂", user=member_user,
            defaults={"desc": "目标示例数据，可删除",
                      "measure": "KG", "goal": 60})
    body_goal, _ = FitGoal.objects.get_or_create(
        name="增肌塑形", user=member_user,
        defaults={"desc": "目标：腹部肌肉明显，可删除",
                  "measure": "体脂率", "goal": 10})
    arm_goal, _ = FitGoal.objects.get_or_create(
        name="手臂围度", user=member_user,
        defaults={"desc": "目标：手臂肌肉围度增加，可删除",
                  "measure": "CM", "goal": 40})
    GoalRecord.objects.filter(user=helper_obj).delete()
    for goal_obj in [lose_goal, body_goal, arm_goal]:
        for i in [7, 6, 5, 4, 3, 2, 1]:
            temp_date = today - datetime.timedelta(days=i)
            new_goal_record = GoalRecord(fit_goal=goal_obj,
                                         user=member_user,
                                         current=goal_obj.goal + i,
                                         cdate=temp_date)
            new_goal_record.save()
    # 添加一条新消息
    new_notify = Notification(
                recipient=user_obj,
                sender=helper_obj,
                action_object_content_type=ContentType.objects.get_for_model(
                    calendar_obj),
                action_object_id=calendar_obj.pk,
                title="欢迎加入Fitahol，竭诚为您服务。",
                description="系统陆续更新中，有任何意见欢迎您通过微信公众号 meta-fitness 告诉我们。",
                show_time=new_event.ctime
            )
    new_notify.save()

# @periodic_task(run_every=timedelta(seconds=10))
# def periodic_test():
#     return ' i running periodic task '
