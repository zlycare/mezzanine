# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2017-09-21 14:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0009_auto_20170920_0627'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogpost',
            name='source_name',
            field=models.CharField(blank=True, default='', help_text='\u6b64\u5904\u586b\u5199\u6587\u7ae0\u6765\u6e90\uff0c\u6bd4\u5982\u201c39\u5065\u5eb7\u7f51\u201d\uff0c\u4ee5\u4fbfApp\u7aef\u5c55\u793a', max_length=100, null=True, verbose_name='\u6587\u7ae0\u6765\u6e90'),
        ),
    ]