#!/usr/bin/env python
# coding=utf-8
"""

__created__ = '1/1/2016'
__author__ = 'deling.ma'
"""
from django.contrib.auth import get_user_model
from rest_framework import serializers
from account.models import Coach, Member, Figure, \
    WechatInfo, Profile, UserRelationConfirm
from fitness.serializers import ExpertTagSerializer, FitGoalSerializer
from gym.serializers import GymnasiumSerializer


class UserSerializer(serializers.ModelSerializer):
    nickname = serializers.CharField(source="profile.nickname")
    portrait = serializers.CharField(source="profile.portrait_url")
    gender = serializers.CharField(source="profile.gender")
    # age = serializers.CharField(source="profile.age")
    # weight = serializers.CharField(source="profile.weight")
    # height = serializers.CharField(source="profile.height")
    u_type = serializers.CharField(source="profile.u_type", read_only=True)
    phone = serializers.CharField(source="profile.phone", read_only=True)
    intro = serializers.CharField(source="profile.intro")

    class Meta:
        model = get_user_model()
        fields = ("date_joined", "id", "portrait", "gender", "phone",
                  "u_type", "nickname", "intro")


class UserInfoSerializer(serializers.ModelSerializer):
    nickname = serializers.CharField(source="profile.nickname")
    portrait = serializers.CharField(source="profile.portrait_url")
    intro = serializers.CharField(source="profile.intro")
    gender = serializers.CharField(source="profile.gender")
    user_id = serializers.IntegerField(source="id")

    class Meta:
        model = get_user_model()
        fields = ("id", "nickname", "portrait", "user_id", "intro", "gender")


class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = ["nickname", "weight", "height", "age", "gender",
                  "intro", "portrait"]


class UserRelationConfirmSerializer(serializers.ModelSerializer):
    sender = UserInfoSerializer()
    recipient = UserInfoSerializer()

    class Meta:
        model = UserRelationConfirm
        exclude = ["utime"]


class CoachSerializer(serializers.ModelSerializer):
    gym = GymnasiumSerializer()
    expert_tags = ExpertTagSerializer(many=True, read_only=True)
    user = UserInfoSerializer()

    class Meta:
        model = Coach
        exclude = ("utime", "ctime", "experience")


class MemberDetailSerializer(serializers.ModelSerializer):
    fit_goal = FitGoalSerializer(read_only=True, many=True)
    user = UserSerializer()
    gym = GymnasiumSerializer()

    class Meta:
        model = Member
        exclude = ("coach", "utime", "ctime", "id", "intro")


class MemberSerializer(serializers.ModelSerializer):
    fit_goal = FitGoalSerializer(read_only=True, many=True)
    gym = GymnasiumSerializer()

    class Meta:
        model = Member
        exclude = ("coach", "utime", "ctime", "id", "user")


class MemberListSerializer(serializers.ModelSerializer):
    nickname = serializers.CharField(source='get_nickname')
    portrait = serializers.CharField(source='get_portrait')
    gender = serializers.CharField(source='get_gender')
    user_id = serializers.IntegerField(source="user.id")
    first_letter = serializers.CharField(source="pinyin_first_letter")

    class Meta:
        model = Member
        fields = ("user_id", "nickname", "gender", "portrait", "first_letter")


class FigureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Figure
        exclude = ("ctime", "utime")


class WechatInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = WechatInfo
