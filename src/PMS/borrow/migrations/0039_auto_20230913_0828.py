# Generated by Django 3.0 on 2023-09-13 08:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('borrow', '0038_auto_20230913_0824'),
    ]

    operations = [
        migrations.AlterField(
            model_name='borrow',
            name='apply_date',
            field=models.CharField(max_length=10),
        ),
        migrations.AlterField(
            model_name='borrow',
            name='expect_date',
            field=models.CharField(max_length=10),
        ),
    ]
