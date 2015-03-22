# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django.core.validators
import curve.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Curve',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('vessel', models.CharField(max_length=80)),
                ('note', models.CharField(max_length=80)),
                ('equation_slug', models.CharField(blank=True, max_length=80, choices=[(b'trig_13', b'13 variable trig curve'), (b'trig_11', b'11 variable trig curve'), (b'trig_9', b'9 variable trig curve'), (b'trig_7', b'7 variable trig curve'), (b'trig_5', b'5 variable trig curve'), (b'trig_3', b'3 variable trig curve')])),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
            },
            bases=(curve.models.CurveCalculations, models.Model),
        ),
        migrations.CreateModel(
            name='Reading',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ships_head', models.FloatField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(359)])),
                ('deviation', models.FloatField(validators=[django.core.validators.MinValueValidator(-180), django.core.validators.MaxValueValidator(180)])),
                ('curve', models.ForeignKey(to='curve.Curve')),
            ],
            options={
                'ordering': ['ships_head'],
            },
            bases=(models.Model,),
        ),
    ]
