# Generated by Django 3.0 on 2023-06-30 07:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_auto_20230630_1411'),
    ]

    operations = [
        migrations.AddField(
            model_name='unit',
            name='manager',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='unit_manager', to=settings.AUTH_USER_MODEL),
        ),
    ]
