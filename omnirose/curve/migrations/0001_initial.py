# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
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
                ('ships_head', models.FloatField()),
                ('deviation', models.FloatField()),
                ('curve', models.ForeignKey(to='curve.Curve')),
            ],
            options={
                'ordering': ['ships_head'],
            },
            bases=(models.Model,),
        ),
    ]
