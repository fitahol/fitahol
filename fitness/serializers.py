#!/usr/bin/env python
# coding=utf-8
"""

__created__ = '6/16/16'
__author__ = 'deling.ma'
"""
from rest_framework import serializers

from fitness.models import GoalRecord, InBodyRecords, ExerciseCategory, \
    FitnessExercise, FitnessEquipment, FitnessVideo, FitnessPicture, \
    Muscle, ExerciseRecord, ExpertTag, FitGoal


class GoalRecordCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = GoalRecord
        exclude = ("ctime", "utime")


class GoalRecordSerializer(serializers.ModelSerializer):
    # fit_goal = FitGoalSerializer()
    current_desc = serializers.CharField(source="get_current_desc")
    cdate = serializers.CharField(source="get_short_cdate")

    class Meta:
        model = GoalRecord
        exclude = ("ctime", "utime", "fit_goal")


class InBodyRecordsSerializer(serializers.ModelSerializer):
    class Meta:
        model = InBodyRecords
        exclude = ("ctime", "utime")


class FitnessVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = FitnessVideo
        exclude = ("ctime", )


class FitnessPictureSerializer(serializers.ModelSerializer):
    class Meta:
        model = FitnessPicture
        exclude = ("ctime", )


class ExerciseCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ExerciseCategory
        exclude = ("ctime", "utime")


class MuscleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Muscle
        fields = ["name", "en_name", "image", "id"]


class FitnessEquipmentSerializer(serializers.ModelSerializer):
    pictures = FitnessPictureSerializer(many=True, read_only=True)

    class Meta:
        model = FitnessEquipment
        exclude = ("ctime", "utime")


class FitnessExerciseSerializer(serializers.ModelSerializer):
    icon_url = serializers.CharField(source="get_icon_url")
    first_letter = serializers.CharField(source="get_first_letter")

    class Meta:
        model = FitnessExercise
        fields = ("id", "name", "en_name", "icon_url", "is_public", "desc",
                  "first_letter")


class FitnessDetailExerciseSerializer(serializers.ModelSerializer):
    equipment = FitnessEquipmentSerializer(many=True, read_only=True)
    pictures = FitnessPictureSerializer(many=True, read_only=True)
    videos = FitnessVideoSerializer(many=True, read_only=True)
    muscles = MuscleSerializer(many=True, read_only=True)

    class Meta:
        model = FitnessExercise
        exclude = ("ctime", "utime", "category", "user")


class ExpertTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpertTag
        exclude = ("ctime", "utime")


class FitGoalCreateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = FitGoal
        fields = ("name", "measure", "goal", "desc", "is_public", "user",
                  "initial", "schedule")


class FitGoalSerializer(serializers.ModelSerializer):
    user = serializers.JSONField(source="get_user_info")
    
    class Meta:
        model = FitGoal
        fields = ("id", "user", "name", "measure", "goal", "is_public",
                  "desc", "initial", "schedule")


class ExerciseRecordSerializer(serializers.ModelSerializer):
    exercise = FitnessExerciseSerializer()
    event_id = serializers.IntegerField(source="event.id")
    
    class Meta:
        model = ExerciseRecord
        fields = ("id", "event_id", "exercise", "value", "number", "ctime")


class ExerciseRecordCreateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ExerciseRecord
        exclude = ("ctime", "utime", )


class FitnessCreateExerciseSerializer(serializers.ModelSerializer):
    equipment = FitnessEquipmentSerializer(many=True)
    pictures = FitnessPictureSerializer(many=True)
    muscles = MuscleSerializer(many=True)

    class Meta:
        model = FitnessExercise
        fields = ("name", "en_name", "desc", "pictures",
                  "muscles", "equipment", "icon", "unit", "strength", "user")
