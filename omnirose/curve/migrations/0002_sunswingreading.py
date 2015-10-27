# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('curve', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SunSwingReading',
            fields=[
                ('reading_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='curve.Reading')),
                ('compass_reading', models.FloatField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(360)])),
                ('shadow_reading', models.FloatField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(360)])),
                ('utc_datetime', models.DateTimeField()),
                ('latitude', models.FloatField(validators=[django.core.validators.MinValueValidator(-90), django.core.validators.MaxValueValidator(90)])),
                ('longitude', models.FloatField(validators=[django.core.validators.MinValueValidator(-180), django.core.validators.MaxValueValidator(180)])),
                ('pelorus_correction', models.FloatField(validators=[django.core.validators.MinValueValidator(-180), django.core.validators.MaxValueValidator(180)])),
                ('variation', models.FloatField(validators=[django.core.validators.MinValueValidator(-180), django.core.validators.MaxValueValidator(180)])),
            ],
            bases=('curve.reading',),
        ),
    ]
