# coding=utf-8

import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "fitahol.settings")
# from django.test import TestCase
import django
django.setup()

import pypinyin
from fitness.models import FitnessExercise


def main():
    queryset = FitnessExercise.objects.all()
    for each in queryset:
        pinyin_name = "'".join(pypinyin.lazy_pinyin(each.name))
        each.pinyin = pinyin_name
        each.save()
        

if __name__ == "__main__":
    main()
