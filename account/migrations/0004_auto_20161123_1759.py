# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-11-23 17:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_auto_20161110_2135'),
    ]

    operations = [
        migrations.AddField(
            model_name='coachmemberref',
            name='primary',
            field=models.BooleanField(default=False, verbose_name='主教练'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='u_type',
            field=models.SmallIntegerField(choices=[(-1, '未选择'), (0, '学员'), (1, '教练')], default=-1, verbose_name='用户身份'),
        ),
    ]
