# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('curve', '0004_auto_20150321_1612'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='reading',
            options={'ordering': ['ships_head']},
        ),
        migrations.AlterField(
            model_name='reading',
            name='ships_head',
            field=models.FloatField(),
            preserve_default=True,
        ),
    ]
