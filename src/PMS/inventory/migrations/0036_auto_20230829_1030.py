# Generated by Django 3.0 on 2023-08-29 10:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0035_auto_20230818_1621'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='appliedform',
            name='total',
        ),
        migrations.RemoveField(
            model_name='applieditem',
            name='amount',
        ),
        migrations.RemoveField(
            model_name='applieditem',
            name='price',
        ),
        migrations.AlterField(
            model_name='appliedform',
            name='apply_date',
            field=models.CharField(default='2023-08-29', max_length=10),
        ),
    ]
