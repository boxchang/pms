# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2019-02-13 03:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('requests', '0002_auto_20190212_1129'),
    ]

    operations = [
        migrations.AddField(
            model_name='request',
            name='is_test',
            field=models.BooleanField(default=False),
        ),
    ]
