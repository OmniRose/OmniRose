# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('curve', '0002_curve_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='curve',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2015, 3, 21, 14, 41, 8, 892002, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='curve',
            name='note',
            field=models.CharField(default='', max_length=80),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='curve',
            name='vessel',
            field=models.CharField(default='', max_length=80),
            preserve_default=False,
        ),
    ]
