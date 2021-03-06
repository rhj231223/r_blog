# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-08-13 18:35
from __future__ import unicode_literals

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FrontUserModel',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('username', models.CharField(max_length=100)),
                ('_password', models.CharField(max_length=200)),
                ('join_time', models.DateTimeField(auto_now_add=True)),
                ('avatar', models.URLField(blank=True)),
                ('is_active', models.IntegerField(default=1)),
            ],
        ),
    ]
