# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-11-17 15:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='start',
            field=models.DateTimeField(db_index=True, verbose_name='start'),
        ),
        migrations.AlterIndexTogether(
            name='event',
            index_together=set([('coach', 'start', 'end', 'calendar')]),
        ),
    ]