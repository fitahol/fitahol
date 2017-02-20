#!/usr/bin/env python
# coding=utf-8
"""

__created__ = '6/14/16'
__author__ = 'deling.ma'
"""
from fabric.api import local, env, run, cd

env.hosts = ['fitahol.com', '10.45.237.159', 'api.fitahol.com']


def test():
    local("./manage.py test my_app")


def commit():
    local("git add -p && git commit")


def push():
    local("git push")


def prepare_deploy():
    test()
    commit()
    push()


def deploy():
    code_dir = '/home/www/fitaholEnv/fitahol'
    # with settings(warn_only=True):
    #     if run("test -d %s" % code_dir).failed:
    #         run("git clone git@git.oschina.net:lingnck/fitahol.git")
    with cd(code_dir):
        run("git pull")
        # "supervisord -c /etc/supervisord.d/supervisord.conf"
        run("supervisorctl -c /etc/supervisord.d/supervisord.conf restart fitahol")
