# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-07-01 14:01
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('analysis', '0033_add_genomes'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='genomeassembly',
            options={'verbose_name_plural': 'genome assemblies'},
        ),
        migrations.RemoveField(
            model_name='analysis',
            name='genome_assembly',
        ),
        migrations.RemoveField(
            model_name='featurelist',
            name='genome_assembly',
        ),
        migrations.RemoveField(
            model_name='genomicdataset',
            name='genome_assembly',
        ),
        migrations.RenameField(
            model_name='analysis',
            old_name='genome_assembly_new',
            new_name='genome_assembly',
        ),
        migrations.RenameField(
            model_name='featurelist',
            old_name='genome_assembly_new',
            new_name='genome_assembly',
        ),
        migrations.RenameField(
            model_name='genomicdataset',
            old_name='genome_assembly_new',
            new_name='genome_assembly',
        ),
        migrations.AlterField(
            model_name='analysis',
            name='genome_assembly',
            field=models.ForeignKey(default=-1, on_delete=django.db.models.deletion.CASCADE, to='analysis.GenomeAssembly'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='featurelist',
            name='genome_assembly',
            field=models.ForeignKey(default=-1, on_delete=django.db.models.deletion.CASCADE, to='analysis.GenomeAssembly'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='genomicdataset',
            name='genome_assembly',
            field=models.ForeignKey(default=-1, on_delete=django.db.models.deletion.CASCADE, to='analysis.GenomeAssembly'),
            preserve_default=False,
        ),
    ]