# Generated by Django 3.0 on 2023-07-03 01:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='itemcategory',
            name='catogory_code',
            field=models.CharField(max_length=2),
        ),
        migrations.AlterField(
            model_name='itemtype',
            name='type_code',
            field=models.CharField(max_length=2),
        ),
    ]
