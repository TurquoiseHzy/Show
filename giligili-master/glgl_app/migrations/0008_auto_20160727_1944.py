# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-07-27 11:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('glgl_app', '0007_auto_20160727_1659'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='time',
        ),
        migrations.AddField(
            model_name='comment',
            name='like',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='comment',
            name='content',
            field=models.CharField(max_length=100),
        ),
    ]
