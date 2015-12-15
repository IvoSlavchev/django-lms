# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('owner', models.CharField(max_length=30)),
                ('name', models.CharField(unique=True, db_index=True, max_length=30)),
                ('description', models.TextField()),
                ('created', models.DateTimeField(default=datetime.datetime.now)),
            ],
        ),
    ]
