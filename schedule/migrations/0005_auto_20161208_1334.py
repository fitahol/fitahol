# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-12-08 13:34
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0004_purchasecourse_gym'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='purchasecourse',
            unique_together=set([('user', 'gym')]),
        ),
    ]
