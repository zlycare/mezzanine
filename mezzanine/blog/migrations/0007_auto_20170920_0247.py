# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2017-09-20 02:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_auto_20170920_0245'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogpost',
            name='source_name',
            field=models.TextField(blank=True, default=None, verbose_name='source_name'),
        ),
    ]
