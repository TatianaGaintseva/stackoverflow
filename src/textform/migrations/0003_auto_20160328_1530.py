# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-28 15:30
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('textform', '0002_message_mod_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='published',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='message',
            name='mod_date',
            field=models.DateTimeField(default=datetime.datetime(2016, 3, 28, 15, 30, 52, 906068, tzinfo=utc), verbose_name='\u0414\u0430\u0442\u0430 \u043f\u043e\u0441\u043b\u0435\u0434\u043d\u0435\u0439 \u043c\u043e\u0434\u0438\u0444\u0438\u043a\u0430\u0446\u0438\u0438'),
        ),
    ]