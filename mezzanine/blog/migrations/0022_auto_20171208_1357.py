# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-12-08 05:57
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import mptt.fields


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0021_auto_20171206_1459'),
    ]

    operations = [
        migrations.CreateModel(
            name='Area',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=50)),
                ('name', models.CharField(max_length=50, unique=True)),
                ('lft', models.PositiveIntegerField(db_index=True, editable=False)),
                ('rght', models.PositiveIntegerField(db_index=True, editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(db_index=True, editable=False)),
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='blog.Area', verbose_name='\u4e0a\u7ea7\u533a\u57df')),
            ],
            options={
                'verbose_name': '\u7701/\u5e02/\u5730\u533a(\u53bf)',
                'verbose_name_plural': '\u7701/\u5e02/\u5730\u533a(\u53bf)',
            },
        ),
        migrations.AddField(
            model_name='blogpost',
            name='areas',
            field=models.ManyToManyField(blank=True, help_text='<strong>\u4e0d\u9009\u5219\u9ed8\u8ba4\u5168\u56fd\u63a8\u5e7f,\u9009\u62e9\u540e\u53ea\u63a8\u5e7f\u6240\u9009\u5730\u533a\uff0c\u5168\u7701\u63a8\u5e7f\u53ef\u53ea\u9009\u62e9\u2018\u7701\u2019<strong/><br/><br/>', related_name='blogposts', to='blog.Area', verbose_name='\u63a8\u5e7f\u5730\u533a'),
        ),
    ]