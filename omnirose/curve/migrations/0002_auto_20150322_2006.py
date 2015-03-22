# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('curve', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='curve',
            name='note',
            field=models.CharField(max_length=80, blank=True),
            preserve_default=True,
        ),
    ]
