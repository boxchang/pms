# Generated by Django 3.0 on 2023-02-07 02:22

import ckeditor_uploader.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('requests', '0002_auto_20221118_2345'),
    ]

    operations = [
        migrations.CreateModel(
            name='Request_reply',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('desc', ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True)),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('create_by', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='request_reply_create_at', to=settings.AUTH_USER_MODEL)),
                ('request', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='request_reply', to='requests.Request')),
            ],
        ),
    ]
