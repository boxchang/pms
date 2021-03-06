# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-12-10 08:16
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('projects', '0001_initial'),
        ('bases', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='status',
            name='create_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='status_create_at', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='status',
            name='update_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='status_update_at', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='dataindex',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='index_project', to='projects.Project'),
        ),
    ]
