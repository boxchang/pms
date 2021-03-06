# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2019-02-12 03:29
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('requests', '0001_initial'),
        ('bugs', '0002_bug_belong_to'),
        ('projects', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('bases', '0002_auto_20190212_1129'),
    ]

    operations = [
        migrations.AddField(
            model_name='bug',
            name='create_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='bug_create_at', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='bug',
            name='level',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='bus_level', to='requests.Level'),
        ),
        migrations.AddField(
            model_name='bug',
            name='owner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='bugs', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='bug',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bug_project', to='projects.Project'),
        ),
        migrations.AddField(
            model_name='bug',
            name='status',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='bug_status', to='bases.Status'),
        ),
        migrations.AddField(
            model_name='bug',
            name='update_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='bug_update_at', to=settings.AUTH_USER_MODEL),
        ),
    ]
