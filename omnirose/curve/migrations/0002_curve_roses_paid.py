# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('curve', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='curve',
            name='roses_paid',
            field=models.DateTimeField(null=True, editable=False, blank=True),
        ),
    ]
