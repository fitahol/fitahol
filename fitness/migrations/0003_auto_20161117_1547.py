# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-11-17 15:47
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fitness', '0002_auto_20161103_0100'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='goalrecord',
            options={'ordering': ('-cdate',), 'verbose_name': '目标更新记录', 'verbose_name_plural': '目标更新记录'},
        ),
    ]
