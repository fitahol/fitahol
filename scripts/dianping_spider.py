#!/usr/bin/env python
# coding=utf-8
"""

__created__ = '1/1/2016'
__author__ = 'deling.ma'
"""
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "fitahol.settings")
import django
django.setup()

import random
import requests
from bs4 import BeautifulSoup

from scripts.agents import AGENTS
from cities.models.dianping import DianPingCity, DianPingDistrict, DianPingGym


def spider_gym():
    start_url = "http://www.dianping.com/search/keyword/1/45_%E5%81%A5%E8%BA%AB%E6%88%BF"
    headers = {'user-agent': random.choice(AGENTS)}
    response = requests.get(start_url, headers=headers)
    if response.status_code != 200:
        print("error: %s" % response.content)
    soup = BeautifulSoup(response.content)

