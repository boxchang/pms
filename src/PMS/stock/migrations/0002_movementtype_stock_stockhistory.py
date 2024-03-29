# Generated by Django 3.2.23 on 2024-03-18 14:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0048_itemfamily_perm_group'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('stock', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MovementType',
            fields=[
                ('mvt_code', models.CharField(max_length=5, primary_key=True, serialize=False)),
                ('mvt_name', models.CharField(max_length=20)),
                ('desc', models.CharField(blank=True, max_length=200, null=True)),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('create_by', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='mvt_create_by', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='StockHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('batch_no', models.CharField(max_length=20)),
                ('mtr_doc', models.CharField(blank=True, max_length=10, null=True)),
                ('plus_qty', models.IntegerField(default=0)),
                ('minus_qty', models.IntegerField(default=0)),
                ('remain_qty', models.IntegerField(default=0)),
                ('desc', models.CharField(blank=True, max_length=200, null=True)),
                ('create_at', models.DateTimeField(auto_now=True, null=True)),
                ('bin', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='stock_hist_bin', to='stock.bin')),
                ('create_by', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='stock_hist_update_by', to=settings.AUTH_USER_MODEL)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='stock_hist_item', to='inventory.item')),
                ('mvt', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='stock_hist_mvt', to='stock.movementtype')),
            ],
        ),
        migrations.CreateModel(
            name='Stock',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qty', models.IntegerField(default=0)),
                ('update_at', models.DateTimeField(auto_now=True, null=True)),
                ('bin', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='stock_bin', to='stock.bin')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='stock_item', to='inventory.item')),
                ('update_by', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='stock_update_by', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
