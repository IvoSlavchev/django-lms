# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.contrib.auth.models
import datetime


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('password', models.CharField(verbose_name='password', max_length=128)),
                ('last_login', models.DateTimeField(verbose_name='last login', blank=True, null=True)),
                ('username', models.CharField(db_index=True, max_length=30, unique=True)),
                ('email', models.EmailField(max_length=30)),
                ('is_teacher', models.BooleanField(default=False)),
                ('date_joined', models.DateTimeField(default=datetime.datetime.now, blank=True)),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
