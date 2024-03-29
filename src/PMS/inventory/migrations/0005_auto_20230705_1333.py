# Generated by Django 3.0 on 2023-07-05 05:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0004_auto_20230703_1604'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='appliedform',
            name='id',
        ),
        migrations.AddField(
            model_name='appliedform',
            name='form_no',
            field=models.AutoField(default=1, primary_key=True, serialize=False),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='appliedform',
            name='apply_date',
            field=models.CharField(default='2023-07-05', max_length=10),
        ),
        migrations.AlterField(
            model_name='appliedform',
            name='reason',
            field=models.CharField(blank=True, max_length=2000, null=True),
        ),
        migrations.AlterField(
            model_name='applieditem',
            name='item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='applied_item', to='inventory.Item'),
        ),
    ]
