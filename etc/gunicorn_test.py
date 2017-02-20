# coding=utf-8
import multiprocessing

bind = '0.0.0.0:7788'
max_requests = 1000
keepalive = 5

proc_name = 'test_fitahol'

workers = 1

loglevel = 'info'
errorlog = '-'

x_forwarded_for_header = 'X-FORWARDED-FOR'
