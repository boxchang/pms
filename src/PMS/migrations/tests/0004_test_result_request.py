# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2019-02-12 06:47
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('requests', '0002_auto_20190212_1129'),
        ('tests', '0003_test_result_result'),
    ]

    operations = [
        migrations.AddField(
            model_name='test_result',
            name='request',
            field=models.ForeignKey(default=16, on_delete=django.db.models.deletion.CASCADE, related_name='test_result_request', to='requests.Request'),
            preserve_default=False,
        ),
    ]
