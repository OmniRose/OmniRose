# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('curve', '0002_curve_roses_paid'),
    ]

    operations = [
        migrations.RenameField(
            model_name='curve',
            old_name='roses_paid',
            new_name='unlocked',
        ),
    ]
