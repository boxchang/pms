# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2019-01-23 05:40
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('requests', '0006_auto_20190123_1338'),
    ]

    operations = [
        migrations.AlterField(
            model_name='request',
            name='owner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='request_owner', to=settings.AUTH_USER_MODEL),
        ),
    ]
