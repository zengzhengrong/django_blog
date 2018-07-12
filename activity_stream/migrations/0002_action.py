# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-07-12 12:10
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contenttypes', '0002_remove_content_type_name'),
        ('activity_stream', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Action',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('verb', models.CharField(max_length=100, verbose_name='动作描述')),
                ('ct_id', models.PositiveIntegerField(blank=True, db_index=True, null=True, verbose_name='动作类型ID')),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='建立时间')),
                ('action_ct', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ct_action', to='contenttypes.ContentType', verbose_name='动作类型')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='actions', to=settings.AUTH_USER_MODEL, verbose_name='动作发出者')),
            ],
            options={
                'verbose_name': '用户动作',
                'verbose_name_plural': '用户动作',
                'ordering': ('-created',),
            },
        ),
    ]
