# Generated by Django 3.0 on 2023-02-10 07:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('problems', '0003_auto_20230210_1458'),
    ]

    operations = [
        migrations.AlterField(
            model_name='problem',
            name='problem_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='problem_type', to='problems.ProblemType'),
        ),
    ]