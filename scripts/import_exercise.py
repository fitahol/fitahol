#!/usr/bin/env python
# coding=utf-8
"""

__created__ = '6/23/16'
__author__ = 'deling.ma'
"""
import os
import csv
import json
from langconv import *
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "fitahol.settings")
import django
django.setup()
from django.core.files import File

from fitness.models import ExerciseCategory, Muscle, ExerciseMuscle, \
    FitnessExercise, FitnessPicture


def exercise_pro_import():
    local_json = {}
    with open("Localizable.json", "r") as lo_file:
        local_json = json.loads(lo_file.read())

    with open("ExercisesPro.csv", newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=';', quotechar=' ')
        for row in spamreader:
            print(row)
            name, musclegroup, primary_muscle, secondary_muscle, icon, image, video, description, skill_level, id = row
            category = ExerciseCategory.objects.get(en_name=musclegroup)
            primary_muscle_obj = Muscle.objects.get(en_name=primary_muscle)
            secondary_muscle_obj = Muscle.objects.get(en_name=secondary_muscle)
            if FitnessExercise.objects.filter(en_name=name).exists():
                continue
            cn_name = local_json.get(name, name)
            print(cn_name)
            desc = local_json.get(description, " ")
            print(desc)
            cn_name = Converter('zh-hans').convert(cn_name)
            desc = Converter('zh-hans').convert(desc)
            icon_path = "output/" + icon + "~iphone.png"
            try:
                icon_img = File(open(icon_path, "rb"))
            except FileNotFoundError:
                icon_img = None
            print(icon_img)
            exercise_obj = FitnessExercise(
                en_name=name, name=cn_name,
                desc=desc,
                category=category, is_public=True,
                icon=icon_img)
            exercise_obj.save()
            try:
                image_1_file = File(open("output/" + image + "-1~iphone.png", "rb"))
                image_1 = FitnessPicture(picture=image_1_file)
                image_1.save()
                exercise_obj.pictures.add(image_1)
            except:
                pass
            try:
                image_2_file = File(open("output/" + image + "-2~iphone.png", "rb"))
                image_2 = FitnessPicture(picture=image_2_file)
                image_2.save()
                exercise_obj.pictures.add(image_2)
            except:
                pass
            primary_ex = ExerciseMuscle(exercise=exercise_obj,
                                        muscle=primary_muscle_obj)
            primary_ex.save()
            secondary_ex = ExerciseMuscle(
                exercise=exercise_obj, muscle=secondary_muscle_obj,
                level="secondary")
            secondary_ex.save()


if __name__ == "__main__":
    exercise_pro_import()
