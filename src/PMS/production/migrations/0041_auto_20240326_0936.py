# Generated by Django 3.2.23 on 2024-03-26 09:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('production', '0040_auto_20240325_1657'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sync_sap_log',
            name='from_series_no',
        ),
        migrations.RemoveField(
            model_name='sync_sap_log',
            name='to_series_no',
        ),
    ]
