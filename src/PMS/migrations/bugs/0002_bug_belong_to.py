# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2019-02-12 03:29
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('requests', '0001_initial'),
        ('bugs', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='bug',
            name='belong_to',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='bug_super', to='requests.Request'),
        ),
    ]
