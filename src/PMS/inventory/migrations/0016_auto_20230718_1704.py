# Generated by Django 3.0 on 2023-07-18 09:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0015_auto_20230717_0835'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appliedform',
            name='apply_date',
            field=models.CharField(default='2023-07-18', max_length=10),
        ),
    ]
