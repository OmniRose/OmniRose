# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('curve', '0003_auto_20150321_1441'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reading',
            name='ships_head',
            field=models.IntegerField(),
            preserve_default=True,
        ),
    ]
