# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-05 03:00
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mhsite', '0004_expense'),
    ]

    operations = [
        migrations.AddField(
            model_name='expense',
            name='month',
            field=models.DateField(default=datetime.datetime(2017, 11, 5, 8, 30, 13, 121321)),
            preserve_default=False,
        ),
    ]
