# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-05 05:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mockup', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='yodlee_login',
            field=models.CharField(default='', max_length=50),
        ),
        migrations.AddField(
            model_name='profile',
            name='yodlee_password',
            field=models.CharField(default='', max_length=50),
        ),
    ]
