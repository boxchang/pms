# Generated by Django 3.0 on 2023-05-22 02:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('borrow', '0007_borrow_admin_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='borrow',
            name='finished',
            field=models.BooleanField(default=False),
        ),
    ]
