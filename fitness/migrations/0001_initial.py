# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-11-03 01:00
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ExerciseCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='中文名称')),
                ('en_name', models.CharField(blank=True, max_length=500, verbose_name='英文名称')),
                ('icon', models.ImageField(blank=True, upload_to='gym/icons', verbose_name='图标')),
                ('ctime', models.DateTimeField(auto_now_add=True)),
                ('utime', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name_plural': '健身大类目',
                'verbose_name': '健身大类目',
                'db_table': 'fitness_category',
            },
        ),
        migrations.CreateModel(
            name='ExerciseMuscle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('level', models.CharField(choices=[('primary', '主肌群'), ('secondary', '附肌群')], default='primary', help_text='一般健身动作包括主肌群和附肌群锻炼; 主肌群示例图片为红色值为primary, 附肌群为蓝色示例图片, 值为secondary', max_length=16, verbose_name='肌群级别')),
                ('ctime', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name_plural': '肌群动作关联表',
                'verbose_name': '肌群动作关联表',
                'db_table': 'exercise_muscle_ref',
            },
        ),
        migrations.CreateModel(
            name='ExerciseRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.IntegerField(default=0, verbose_name='计量值')),
                ('number', models.IntegerField(default=0, verbose_name='次数')),
                ('ctime', models.DateTimeField(auto_now_add=True)),
                ('utime', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'fitness_exercise_record',
                'verbose_name_plural': '健身动作记录',
                'verbose_name': '健身动作记录',
            },
        ),
        migrations.CreateModel(
            name='ExpertTag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=36, unique=True, verbose_name='名称')),
                ('desc', models.CharField(blank=True, max_length=1000, verbose_name='说明')),
                ('is_public', models.BooleanField(default=False, verbose_name='全员可见')),
                ('ctime', models.DateTimeField(auto_now_add=True)),
                ('utime', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name_plural': '教练专长领域',
                'verbose_name': '教练专长领域',
                'db_table': 'expert_tags',
            },
        ),
        migrations.CreateModel(
            name='FitGoal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, verbose_name='目标名称')),
                ('desc', models.CharField(blank=True, max_length=1000, verbose_name='目标描述')),
                ('is_public', models.BooleanField(default=False, verbose_name='全员可见')),
                ('measure', models.CharField(default='Kg', help_text='不同类型健身指标不同', max_length=16, verbose_name='计量单位')),
                ('goal', models.IntegerField(default=0, help_text='不同类型,指标值不同', verbose_name='目标值')),
                ('ctime', models.DateTimeField(auto_now_add=True)),
                ('utime', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': '健身目标',
                'verbose_name': '健身目标',
                'db_table': 'fit_goal',
            },
        ),
        migrations.CreateModel(
            name='FitnessEquipment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='名称')),
                ('desc', models.CharField(blank=True, max_length=500, verbose_name='作用描述')),
                ('cover', models.ImageField(blank=True, null=True, upload_to='gym/equipment', verbose_name='封面')),
                ('ctime', models.DateTimeField(auto_now_add=True)),
                ('utime', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name_plural': '健身设备',
                'verbose_name': '健身设备',
                'db_table': 'fitness_equipment',
            },
        ),
        migrations.CreateModel(
            name='FitnessExercise',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='名称')),
                ('en_name', models.CharField(blank=True, max_length=500, verbose_name='英文名称')),
                ('desc', models.TextField(blank=True, verbose_name='描述')),
                ('icon', models.ImageField(blank=True, null=True, upload_to='gym/exercise_icon', verbose_name='封面')),
                ('unit', models.CharField(default='KG', max_length=16, verbose_name='计量单位')),
                ('strength', models.CharField(blank=True, help_text='和计量单位搭配, 衡量健身动作', max_length=100, verbose_name='强度单位')),
                ('is_public', models.BooleanField(default=False, verbose_name='是否全员可用')),
                ('ctime', models.DateTimeField(auto_now_add=True)),
                ('utime', models.DateTimeField(auto_now=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fitness.ExerciseCategory', verbose_name='分类')),
                ('equipment', models.ManyToManyField(blank=True, to='fitness.FitnessEquipment', verbose_name='使用设备')),
            ],
            options={
                'verbose_name_plural': '健身动作',
                'verbose_name': '健身动作',
                'db_table': 'fitness_exercise',
            },
        ),
        migrations.CreateModel(
            name='FitnessPicture',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('picture', models.ImageField(upload_to='gym/pictures', verbose_name='配图')),
                ('ctime', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name_plural': '健身配图',
                'verbose_name': '健身配图',
                'db_table': 'fitness_pictures',
            },
        ),
        migrations.CreateModel(
            name='FitnessVideo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('video', models.ImageField(upload_to='gym/videos', verbose_name='视频')),
                ('ctime', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name_plural': '健身视频',
                'verbose_name': '健身视频',
                'db_table': 'fitness_videos',
            },
        ),
        migrations.CreateModel(
            name='GoalRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('current', models.IntegerField(default=0, verbose_name='当前值')),
                ('cdate', models.DateField(db_index=True, verbose_name='日期')),
                ('ctime', models.DateTimeField(auto_now_add=True)),
                ('utime', models.DateTimeField(auto_now=True)),
                ('fit_goal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fitness.FitGoal')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': '目标更新记录',
                'ordering': ('cdate',),
                'verbose_name': '目标更新记录',
                'db_table': 'fitness_goal_record',
            },
        ),
        migrations.CreateModel(
            name='InBodyRecords',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cdate', models.DateField(verbose_name='日期')),
                ('weight', models.IntegerField(default=0, verbose_name='体重')),
                ('metabolism', models.IntegerField(default=0, verbose_name='基础代谢')),
                ('body_fat', models.IntegerField(default=0, verbose_name='体脂率')),
                ('fat_weight', models.IntegerField(default=0, verbose_name='脂肪重量')),
                ('skeletal_muscle', models.IntegerField(default=0, verbose_name='骨骼肌')),
                ('chest', models.IntegerField(default=0, verbose_name='胸围')),
                ('arm', models.IntegerField(default=0, verbose_name='臂围')),
                ('upper_arm', models.IntegerField(default=0, verbose_name='上臂围')),
                ('waistline', models.IntegerField(default=0, verbose_name='腰围')),
                ('thigh', models.IntegerField(default=0, verbose_name='大腿围')),
                ('crus', models.IntegerField(default=0, verbose_name='小腿围')),
                ('ctime', models.DateTimeField(auto_now_add=True)),
                ('utime', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'InBody体测机数据记录',
                'verbose_name': 'InBody体测机数据记录',
                'db_table': 'in_body_records',
            },
        ),
        migrations.CreateModel(
            name='Muscle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='中文名称')),
                ('en_name', models.CharField(blank=True, max_length=500, verbose_name='英文名称')),
                ('image', models.ImageField(blank=True, upload_to='gym/muscle', verbose_name='示例图片')),
                ('ctime', models.DateTimeField(auto_now_add=True)),
                ('utime', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name_plural': '肌群分类',
                'verbose_name': '肌群分类',
                'db_table': 'fitness_muscle',
            },
        ),
        migrations.AddField(
            model_name='fitnessexercise',
            name='muscles',
            field=models.ManyToManyField(blank=True, through='fitness.ExerciseMuscle', to='fitness.Muscle'),
        ),
        migrations.AddField(
            model_name='fitnessexercise',
            name='pictures',
            field=models.ManyToManyField(blank=True, to='fitness.FitnessPicture', verbose_name='配图'),
        ),
        migrations.AddField(
            model_name='fitnessexercise',
            name='user',
            field=models.ForeignKey(blank=True, help_text='个人定制', null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='fitnessexercise',
            name='videos',
            field=models.ManyToManyField(blank=True, to='fitness.FitnessVideo', verbose_name='演示视频'),
        ),
        migrations.AddField(
            model_name='fitnessequipment',
            name='pictures',
            field=models.ManyToManyField(blank=True, to='fitness.FitnessPicture'),
        ),
    ]
