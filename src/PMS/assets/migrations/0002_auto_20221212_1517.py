# Generated by Django 3.0 on 2022-12-12 07:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assets', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='label_attachment',
            name='files',
            field=models.FileField(upload_to='uploads/label/'),
        ),
    ]
