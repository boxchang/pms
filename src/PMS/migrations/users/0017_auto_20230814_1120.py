# Generated by Django 3.0 on 2023-08-14 11:20

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0016_auto_20230801_1117'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='mobile_number',
            field=models.CharField(blank=True, help_text='Required. digits and +-() only.', max_length=30, validators=[django.core.validators.RegexValidator('^[0-9+()-]+$', 'Enter a valid mobile number.', 'invalid')], verbose_name='mobile number'),
        ),
    ]