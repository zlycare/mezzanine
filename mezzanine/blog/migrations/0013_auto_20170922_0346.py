# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2017-09-22 03:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0012_blogcategory_suggested_keywords'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blogcategory',
            name='title2',
        ),
        migrations.AddField(
            model_name='blogcategory',
            name='category1',
            field=models.CharField(blank=True, max_length=100, verbose_name='title2'),
        ),
        migrations.AddField(
            model_name='blogcategory',
            name='category2',
            field=models.CharField(blank=True, max_length=100, verbose_name='title2'),
        ),
    ]
