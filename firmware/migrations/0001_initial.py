# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-11-03 01:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ClientVersion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('platform', models.SmallIntegerField(choices=[(0, 'Android'), (1, 'iOS')], default=0, verbose_name='所属平台')),
                ('start_version', models.CharField(default='1.0.0', help_text='版本号必须是 x.x.x 单位数 ', max_length=6, verbose_name='开始版本号')),
                ('end_version', models.CharField(max_length=6, verbose_name='结束版本号')),
                ('version', models.CharField(max_length=6, verbose_name='当前版本')),
                ('desc', models.TextField(verbose_name='升级描述')),
                ('android_url', models.FileField(blank=True, upload_to='firmware/version', verbose_name='Android下载地址')),
                ('ios_url', models.CharField(blank=True, max_length=500, verbose_name='Android下载地址')),
                ('is_force', models.BooleanField(default=False, verbose_name='是否强制升级')),
                ('state', models.SmallIntegerField(choices=[(1, '上线'), (0, '下线')], db_index=True, default=0, verbose_name='状态码')),
                ('ctime', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('utime', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
            ],
            options={
                'verbose_name_plural': '客户端升级升级配置',
                'verbose_name': '客户端升级配置',
                'db_table': 'client_config',
            },
        ),
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nickname', models.CharField(max_length=16, verbose_name='昵称')),
                ('contact', models.CharField(max_length=100, verbose_name='联系方式')),
                ('content', models.CharField(max_length=1000, verbose_name='反馈内容')),
                ('ctime', models.DateTimeField(auto_now=True, verbose_name='创建时间')),
            ],
            options={
                'verbose_name_plural': '用户反馈',
                'verbose_name': '用户反馈',
                'db_table': 'feedback',
            },
        ),
    ]
