# Generated by Django 3.2.23 on 2024-02-29 09:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('production', '0032_record_status'),
    ]

    operations = [
        migrations.RenameField(
            model_name='sync_sap_log',
            old_name='update_at',
            new_name='create_at',
        ),
        migrations.RenameField(
            model_name='sync_sap_log',
            old_name='update_by',
            new_name='create_by',
        ),
    ]