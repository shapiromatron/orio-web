# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-01-11 21:00
from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('analysis', '0008_auto_20160108_1649'),
    ]

    operations = [
        migrations.AddField(
            model_name='encodedataset',
            name='extra_content',
            field=django.contrib.postgres.fields.jsonb.JSONField(default=dict),
        ),
    ]