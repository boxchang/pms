# Generated by Django 3.0 on 2022-12-21 06:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('assets', '0017_auto_20221221_1442'),
    ]

    operations = [
        migrations.AlterField(
            model_name='asset',
            name='keeper_unit',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='asset_keeper_unit', to='assets.Unit'),
        ),
        migrations.AlterField(
            model_name='asset',
            name='owner_unit',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='asset_owner_unit', to='assets.Unit'),
        ),
    ]
