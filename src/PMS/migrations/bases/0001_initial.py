# Generated by Django 3.0 on 2022-11-18 15:45

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DataIndex',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_type', models.CharField(max_length=10)),
                ('data_date', models.CharField(max_length=8)),
                ('current', models.IntegerField(blank=True, default=0, null=True)),
                ('update_at', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='FormType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tid', models.IntegerField()),
                ('type', models.CharField(max_length=8)),
                ('short_name', models.CharField(max_length=3)),
            ],
        ),
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status_en', models.CharField(max_length=50)),
                ('status_cn', models.CharField(max_length=50)),
                ('status_desc', models.TextField()),
                ('process_rate', models.IntegerField(default=0)),
                ('create_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('update_at', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
    ]
