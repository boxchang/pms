# Generated by Django 3.0 on 2023-10-23 11:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assets', '0027_assetcategory_perm_group'),
    ]

    operations = [
        migrations.AddField(
            model_name='asset',
            name='label_no',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]