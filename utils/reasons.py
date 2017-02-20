#!/usr/bin/env python
# coding=utf-8
"""
定义 http code desc

400 客户端错误判断常用, 参数格式错误例外

出现同http status歧义时也会使用.

__created__ = '27/1/2016'
__author__ = 'deling.ma'
"""
CODE_10000_OK = 10000

CODE_HEADER_10000 = {"code-desc": "Ok"}

CODE_10001_EXISTS = 10001

CODE_HEADER_10001 = {"code-desc": "account exists"}

CODE_10002_UNFOUNDED = 10002

CODE_HEADER_10002 = {"code-desc": "account unfounded"}

CODE_10003_PWD = 10003

CODE_HEADER_10003 = {"code-desc": "pwd error"}

CODE_10004_VCODE = 10004

CODE_HEADER_10004 = {"code-desc": "vCODE error"}

