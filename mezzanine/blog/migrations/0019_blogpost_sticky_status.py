# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-11-08 06:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0018_blogpost_collect_count'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogpost',
            name='sticky_status',
            field=models.IntegerField(choices=[(0, '\u672a\u7f6e\u9876'), (1, '\u5df2\u7f6e\u9876')], default=0, verbose_name='\u7f6e\u9876\u72b6\u6001'),
        ),
    ]
