# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='SunSwing',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('vessel', models.CharField(help_text=b'e.g. "SV Gypsy Moth"', max_length=80, verbose_name=b"Vessel's Name")),
                ('note', models.CharField(help_text=b'e.g. "Steering compass"', max_length=80, verbose_name=b'Note', blank=True)),
                ('video_start_time', models.DateTimeField()),
                ('latitude', models.FloatField(validators=[django.core.validators.MinValueValidator(-90), django.core.validators.MaxValueValidator(90)])),
                ('longitude', models.FloatField(validators=[django.core.validators.MinValueValidator(-180), django.core.validators.MaxValueValidator(180)])),
                ('pelorus_correction', models.FloatField(validators=[django.core.validators.MinValueValidator(-180), django.core.validators.MaxValueValidator(180)])),
                ('variation', models.FloatField(validators=[django.core.validators.MinValueValidator(-180), django.core.validators.MaxValueValidator(180)])),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['vessel', 'note'],
            },
        ),
        migrations.CreateModel(
            name='SunSwingReading',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('video_time', models.FloatField(verbose_name=django.core.validators.MinValueValidator(0))),
                ('compass_reading', models.FloatField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(360)])),
                ('shadow_reading', models.FloatField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(360)])),
                ('sun_swing', models.ForeignKey(related_name='reading_set', to='swing.SunSwing')),
            ],
            options={
                'ordering': ['video_time'],
            },
        ),
    ]
