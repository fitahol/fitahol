#!/usr/bin/env python
# coding=utf-8
"""

__created__ = '6/16/16'
__author__ = 'deling.ma'
"""
from rest_framework import routers

from fitness import views

router = routers.DefaultRouter()
router.register(r'category', views.ExerciseCategoryViewSet)
router.register(r'muscle', views.MuscleViewSet)
router.register(r'exercise', views.FitnessExerciseViewSet)
router.register(r'equipment', views.FitnessEquipmentViewSet)
router.register(r'exercise_record', views.ExerciseRecordViewSet)
router.register(r'inbody', views.InBodyRecordsViewSet)
router.register(r'expert_tag', views.ExpertTagViewSet)
router.register(r'fit_goal', views.FitGoalViewSet)
router.register(r'goal_record', views.GoalRecordViewSet)

urlpatterns = router.urls
