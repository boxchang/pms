# Generated by Django 3.0 on 2023-06-16 02:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('borrow', '0009_auto_20230612_0843'),
    ]

    operations = [
        migrations.AlterField(
            model_name='borrow',
            name='apply_date',
            field=models.CharField(default='2023-06-16', max_length=10),
        ),
        migrations.AlterField(
            model_name='borrow',
            name='expect_date',
            field=models.CharField(default='2023-06-16', max_length=10),
        ),
    ]
