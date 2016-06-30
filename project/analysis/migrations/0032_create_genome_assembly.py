# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-30 20:59
from __future__ import unicode_literals

from django.db import migrations, models
import orio.utils
import utils.models


class Migration(migrations.Migration):

    dependencies = [
        ('analysis', '0031_auto_20160630_1017'),
    ]

    operations = [
        migrations.CreateModel(
            name='GenomeAssembly',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('chromosome_size_file', utils.models.DynamicFilePathField(max_length=128, path=orio.utils.get_data_path)),
            ],
        ),
    ]
