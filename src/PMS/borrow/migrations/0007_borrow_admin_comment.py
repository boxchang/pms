# Generated by Django 3.0 on 2023-05-12 02:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('borrow', '0006_auto_20230504_1632'),
    ]

    operations = [
        migrations.AddField(
            model_name='borrow',
            name='admin_comment',
            field=models.CharField(default='', max_length=500),
            preserve_default=False,
        ),
    ]
