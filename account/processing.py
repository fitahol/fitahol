#!/usr/bin/env python
# coding=utf-8
"""

__created__ = '13/1/2016'
__author__ = 'deling.ma'
"""


def get_username(account):
    if account.isdigit():
        return "phone", account
    else:
        username = "@".join([account.split("@")[0],
                             account.split("@")[-1].split(".")[0]])
        return "email", username
