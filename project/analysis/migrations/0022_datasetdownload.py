# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-04-18 20:50
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('analysis', '0021_auto_20160418_1506'),
    ]

    operations = [
        migrations.CreateModel(
            name='DatasetDownload',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField()),
                ('filename', models.CharField(help_text='Filename (no extension)', max_length=100)),
                ('status_code', models.PositiveSmallIntegerField(choices=[(0, 'not-started'), (1, 'started'), (2, 'finished with errors'), (3, 'successfully completed')], default=0)),
                ('status', models.TextField(blank=True, null=True)),
                ('start_time', models.DateTimeField(blank=True, null=True)),
                ('end_time', models.DateTimeField(blank=True, null=True)),
                ('owner', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='datasetdownload', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
