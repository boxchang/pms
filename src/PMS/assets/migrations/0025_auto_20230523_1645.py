# Generated by Django 3.0 on 2023-05-23 08:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assets', '0024_auto_20230407_0918'),
    ]

    operations = [
        migrations.AddField(
            model_name='assettype',
            name='prefix',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='assettype',
            name='series_len',
            field=models.IntegerField(default=5),
        ),
    ]
