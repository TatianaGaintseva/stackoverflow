# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-06 12:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='\u0418\u043c\u044f \u0431\u043b\u043e\u0433\u0430')),
                ('descr', models.CharField(max_length=500, verbose_name='\u041a\u0440\u0430\u0442\u043a\u043e\u0435 \u043e\u043f\u0438\u0441\u0430\u043d\u0438\u0435')),
            ],
        ),
    ]
