#!/usr/bin/env python
# coding=utf-8
"""

__created__ = '4/8/16'
__author__ = 'deling.ma'
"""
DEBUG = True

# Online DB
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'fitahol',
        'USER': 'fitahol_www',
        'PASSWORD': 'fitaholwww',
        'HOST': 'rds45lxm19p0jzjb3ts9.mysql.rds.aliyuncs.com',
        'PORT': '3306',
        'CHARSET': 'utf8',
        'OPTIONS': {
            'init_command': 'SET storage_engine=INNODB, sql_mode=STRICT_TRANS_TABLES',
        },
    }
}

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'fitahol',
#         'USER': 'root',
#         'PASSWORD': 'root',
#         'HOST': '127.0.0.1',
#         'PORT': '3306',
#         'CHARSET': 'utf8',
#         'OPTIONS': {
#             'init_command': 'SET storage_engine=INNODB',
#         },
#     }
# }

# 跨域配置
CORS_ORIGIN_WHITELIST = ("127.0.0.1:3000",
                         "127.0.0.1:2211",
                         "192.168.199.101:3000",
                         "192.168.198.191:3000",
                         "192.168.199.101:2016")

