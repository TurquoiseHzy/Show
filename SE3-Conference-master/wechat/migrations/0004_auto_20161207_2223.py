# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-12-07 14:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wechat', '0003_auto_20161207_2059'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='all_conf_page',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='user',
            name='my_conf_page',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='user',
            name='upcoming_conf_page',
            field=models.IntegerField(default=1),
        ),
    ]
