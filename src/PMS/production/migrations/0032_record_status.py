# Generated by Django 3.2.23 on 2024-02-27 15:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('production', '0031_sync_sap_log_sync_sap_series'),
    ]

    operations = [
        migrations.AddField(
            model_name='record',
            name='status',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]