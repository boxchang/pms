# Generated by Django 3.0 on 2023-08-11 10:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0029_auto_20230810_1651'),
    ]

    operations = [
        migrations.AddField(
            model_name='itemcategory',
            name='manual',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='itemtype',
            name='is_attached',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='appliedform',
            name='apply_date',
            field=models.CharField(default='2023-08-11', max_length=10),
        ),
    ]