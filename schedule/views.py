#!/usr/bin/env python
# coding=utf-8
"""

__created__ = '31/1/2016'
__author__ = 'deling.ma'
"""
import datetime

from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.decorators import list_route, detail_route
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from account.models import Coach, CoachMemberRef
from schedule.models import Event, Calendar, Rule, PurchaseCourse
from schedule.serializers import EventSerializer, CalendarSerializer, \
    EventCreateSerializer, RuleSerializer, PurchaseCourseSerializer, \
    CoachEventSerializer
from schedule.tasks import event_rule_task


class CalendarViewSet(viewsets.ModelViewSet):
    queryset = Calendar.objects.all()
    serializer_class = CalendarSerializer
    pagination_class = None


class RuleViewSet(viewsets.ModelViewSet):
    queryset = Rule.objects.all()
    serializer_class = RuleSerializer
    pagination_class = None


class PurchaseCourseViewSet(viewsets.ModelViewSet):
    queryset = PurchaseCourse.objects.all()
    serializer_class = PurchaseCourseSerializer
    pagination_class = None
    permission_classes = (IsAuthenticated,)
    
    def create(self, request, *args, **kwargs):
        user_id = self.request.data["user_id"]
        remain = int(self.request.data["remain"])
        coach_obj = Coach.objects.get(user=request.user)
        try:
            course_obj = PurchaseCourse.objects.get(user_id=user_id,
                                                    gym=coach_obj.gym)
            course_obj.amount += remain
            course_obj.remain += remain
            course_obj.save()
        except PurchaseCourse.DoesNotExist:
            new_course = PurchaseCourse(amount=remain, remain=remain,
                                        user_id=user_id, gym=coach_obj.gym)
            new_course.save()
        return Response({"detail": "修改课程成功"})
    
    @list_route()
    def purchased(self, request, *args, **kwargs):
        user_id = self.request.query_params["user_id"]
        queryset = CoachMemberRef.objects.filter(member__user__id=user_id,
                                                 primary=True)
        gym = None
        if queryset:
            gym = queryset[0].coach.gym
        try:
            instance = PurchaseCourse.objects.get(user_id=user_id, gym=gym)
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        except PurchaseCourse.DoesNotExist:
            return Response({"user_id": user_id, "amount": 0, "remain": 0})


class EventViewSet(viewsets.ModelViewSet):
    """日程事件"""
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    pagination_class = None
    permission_classes = (IsAuthenticated,)
    
    def get_serializer_class(self):
        if self.request.method == "POST":
            return EventCreateSerializer
        coach_event = self.request.query_params.get("coach_event")
        interval = self.request.query_params.get("interval")
        user_id = self.request.query_params.get("user_id")
        if coach_event:
            # 学员端 预约课程页获取
            return CoachEventSerializer
        elif user_id and not interval:
            # 学员 历史课程获取
            return CoachEventSerializer
        else:
            return EventSerializer
    
    @detail_route(methods=['put'])
    def state(self, request, *args, **kwargs):
        state = request.data.get("state", 1)  # 默认结课
        instance = Event.objects.get(id=self.kwargs["pk"])
        instance.state = state
        instance.save()
        if state == 1:
            # 结课： 消耗一节课
            course_obj = PurchaseCourse.objects.filter(
                user=instance.user, gym=instance.coach.gym)
            course_obj.remain -= 1
            course_obj.save()
        elif state == -1:
            # 拒绝 预约课程
            instance.delete()
        return Response({"detail": "操作成功"})
    
    @list_route(methods=['get'])
    def last(self, request, *args, **kwargs):
        user_id = self.request.query_params["user_id"]
        calendar_slug = self.request.query_params.get("calendar", "default")
        now = datetime.datetime.now()
        event = Event.objects.filter(calendar__slug=calendar_slug,
                                     user_id=user_id, start__gte=now).last()
        if not event:
            return Response({}, status=status.HTTP_204_NO_CONTENT)
        serializer = EventSerializer(event)
        return Response(serializer.data)
    
    def create(self, request, *args, **kwargs):
        request_data = request.data.copy()
        calendar_slug = request_data.get("calendar_slug", "default")
        start = request_data["start"]
        end = request_data["end"]
        if start[-5:] not in ["00:00", "30:00"]:
            return Response({"detail": "开始时间只允许整点或半点"},
                            status=status.HTTP_400_BAD_REQUEST)
        start_date = datetime.datetime.strptime(start, "%Y-%m-%d %H:%M:%S")
        end_date = datetime.datetime.strptime(end, "%Y-%m-%d %H:%M:%S")
        diff = (end_date - start_date)
        if calendar_slug != "rest" and \
                (diff.total_seconds() < 3600.0 or diff.total_seconds() > 10800.0):
            return Response({"detail": "单节课只能1至3小时"},
                            status=status.HTTP_400_BAD_REQUEST)
        if Event.objects.filter(start__lt=start_date, start__gt=end_date,
                                coach_id=request_data["coach"]).exists():
            return Response({"detail": "该时段已有课程"},
                            status=status.HTTP_400_BAD_REQUEST)
        if Event.objects.filter(end__lt=start_date, end__gt=end_date,
                                coach_id=request_data["coach"]).exists():
            return Response({"detail": "已存在其他课程"},
                            status=status.HTTP_400_BAD_REQUEST)
        if Event.objects.filter(start__gte=start_date, end__lte=end_date,
                                coach_id=request_data["coach"]).exists():
            return Response({"detail": "该时段包含其他课程"},
                            status=status.HTTP_400_BAD_REQUEST)
        
        if calendar_slug == "rest":
            # 设置休息时段
            try:
                user_obj = get_user_model().objects.get(username="rest")
                request_data["user_id"] = user_obj.id
                request_data["state"] = -1
            except get_user_model().DoesNotExist:
                return Response({"detail": "未配置休息信息"},
                                status=status.HTTP_400_BAD_REQUEST)
        
        reserve = request_data.get("reserve")
        if reserve:
            # 课程预约
            request_data["state"] = 2
            request_data["rule"] = ""  # 获取不允许设置规则
        request_data["calendar"] = Calendar.objects.get(slug=calendar_slug).id
        request_data["user"] = request_data["user_id"]
        if request_data["user"] == request_data["coach"]:
            return Response({"detail": "不能为自己添加课程"},
                            status=status.HTTP_400_BAD_REQUEST)
        end_recurring_period = request_data.get("end_recurring_period")
        if not end_recurring_period:
            try:
                del request_data["end_recurring_period"]
            except KeyError:
                pass
        rule_id = int(request_data.get("rule_id", 0))
        if rule_id:
            if not end_recurring_period and not request_data.get("times"):
                return Response({"detail": "重复事件需要选择次数或终止时间"},
                                status=status.HTTP_400_BAD_REQUEST)
            request_data["rule"] = rule_id
            try:
                times = int(request_data.get("times")) or 100
            except TypeError:
                times = 100
            request_data["times"] = times
            if not end_recurring_period:
                today = datetime.datetime.today()
                next_year = today.replace(year=today.year + 1)
                request_data["end_recurring_period"] = next_year
        serializer = self.get_serializer(data=request_data)
        serializer.is_valid(raise_exception=True)
        result = serializer.save()
        event_rule_task.delay(result.id)
        return Response({"detail": "创建成功"}, status=status.HTTP_201_CREATED)
    
    def get_queryset(self):
        interval = self.request.query_params.get("interval")
        user_id = self.request.query_params.get("user_id")
        if user_id and not interval:
            # 学员历史课程获取
            return Event.objects.filter(user_id=user_id)
        user_obj = self.request.user
        if user_id:
            user_obj = get_user_model().objects.get(id=user_id)
        if interval == "date":
            date = self.request.query_params["date"]
            queryset = Event.objects.filter(start__startswith=date,
                                            coach=user_obj)
        elif interval == "date_range":
            begin = self.request.query_params["begin"]
            end = self.request.query_params["end"]
            end_date = datetime.datetime.strptime(
                end, '%Y-%m-%d') + datetime.timedelta(days=1)
            queryset = Event.objects.filter(start__gte=begin,
                                            end__lte=end_date,
                                            coach=user_obj)
        elif interval == "month":
            year = self.request.query_params["year"]
            month = self.request.query_params["month"]
            queryset = Event.objects.filter(start__year=year, start_month=month,
                                            coach=user_obj)
        elif interval == "year":
            year = self.request.query_params["year"]
            queryset = Event.objects.filter(start__year=year,
                                            coach=user_obj)
        else:
            return Event.objects.all()
        # calendar_slug = self.request.query_params.get("calendar")
        # if calendar_slug:
        #     calendar_obj = Calendar.objects.get(slug=calendar_slug)
        #     queryset = queryset.filter(calendar=calendar_obj)
        coach_event = self.request.query_params.get("coach_event")
        if coach_event:
            # 学员端 预约课程页获取
            return queryset.filter(user=self.request.user)
        return queryset


class EventAnalyticsView(APIView):
    permission_classes = (IsAuthenticated,)
    
    def get(self, request, *args, **kwargs):
        user_obj = self.request.user
        end = datetime.datetime.today()
        week_begin = end - datetime.timedelta(days=7)
        month_begin = end - datetime.timedelta(days=30)
        week_queryset = Event.objects.filter(start__gte=week_begin,
                                             end__lte=end,
                                             coach=user_obj,
                                             state=1,
                                             calendar__slug="default")
        week_count = week_queryset.count()
        weekday_report = []
        for i in range(7):
            temp_date = end - datetime.timedelta(days=i)
            end_date = end + datetime.timedelta(days=1)
            temp_count = Event.objects.filter(start__gte=temp_date,
                                              end__lte=end_date,
                                              coach=user_obj,
                                              state=1,
                                              calendar__slug="default").count()
            weekday_report.append({"cdate": temp_date.strftime('%m-%d'),
                                   "count": temp_count})
        month_queryset = Event.objects.filter(start__gte=month_begin,
                                              end__lte=end,
                                              coach=user_obj,
                                              state=1,
                                              calendar__slug="default")
        month_count = month_queryset.count()
        event_total = Event.objects.filter(coach=user_obj,
                                           calendar__slug="default").count()
        event_remain = Event.objects.filter(coach=user_obj, state=1).count()
        return Response({"weekday_report": weekday_report,
                         "event_total": event_total,
                         "event_remain": event_remain,
                         "week_count": week_count,
                         "month_count": month_count})
