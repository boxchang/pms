# Generated by Django 3.0 on 2023-09-13 08:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('borrow', '0037_auto_20230911_1314'),
    ]

    operations = [
        migrations.AlterField(
            model_name='borrow',
            name='apply_date',
            field=models.CharField(default='2023-09-13', max_length=10),
        ),
        migrations.AlterField(
            model_name='borrow',
            name='expect_date',
            field=models.CharField(default='2023-09-13', max_length=10),
        ),
    ]
