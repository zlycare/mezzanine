# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2017-09-20 02:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_auto_20170919_0733'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blogpost',
            name='trans_count',
        ),
        migrations.AddField(
            model_name='blogpost',
            name='repost_count',
            field=models.IntegerField(blank=True, default=0, verbose_name='repost_count'),
        ),
        migrations.AddField(
            model_name='blogpost',
            name='source_name',
            field=models.IntegerField(blank=True, default=0, verbose_name='source_name'),
        ),
    ]
