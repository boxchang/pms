# Generated by Django 3.2.23 on 2024-03-18 16:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assets', '0031_alter_history_asset'),
    ]

    operations = [
        migrations.AlterField(
            model_name='asset',
            name='label_no',
            field=models.CharField(blank=True, max_length=50, null=True, unique=True),
        ),
    ]