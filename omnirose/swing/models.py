from datetime import datetime, timedelta
from astral import Astral

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from accounts.models import User

from geomag import declination

def norm360(angle):
    while angle < 0:
        angle = angle + 360
    return angle % 360

class SunSwing(models.Model):
    user = models.ForeignKey(User)

    vessel = models.CharField(
        max_length=80,
        verbose_name="Vessel's Name",
        help_text='e.g. "SV Gypsy Moth"',
    )
    note = models.CharField(
        max_length=80,
        blank=True,
        verbose_name="Note",
        help_text='e.g. "Steering compass"',
    )

    video_start_time = models.DateTimeField()

    latitude  = models.FloatField(validators=[MinValueValidator(-90),  MaxValueValidator(90)])
    longitude = models.FloatField(validators=[MinValueValidator(-180), MaxValueValidator(180)])

    pelorus_correction = models.FloatField(validators=[MinValueValidator(-180), MaxValueValidator(180)])

    variation = models.FloatField(validators=[MinValueValidator(-180), MaxValueValidator(180)])

    def save(self, *args, **kwargs):
        if not self.variation:
            variation = declination(dlat=self.latitude, dlon=self.longitude, time=self.video_start_time.date())
            variation = float("{0:.2f}".format(variation))
            self.variation = variation
        super(SunSwing, self).save(*args, **kwargs)

    def solar_azimuth_at(self, when):
        return Astral().solar_azimuth(when, self.latitude, self.longitude)

    def __unicode__(self):
        return u"%s (%s)" % (self.vessel, self.note)

    class Meta():
        ordering = ['vessel', 'note']



class SunSwingReading(models.Model):
    sun_swing = models.ForeignKey(SunSwing, related_name="reading_set")
    video_time = models.FloatField(MinValueValidator(0))
    compass_reading = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(360)])
    shadow_reading = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(360)])


    @property
    def utc_datetime(self):
        return self.sun_swing.video_start_time + timedelta(seconds=self.video_time)

    @property
    def solar_azimuth(self):
        return self.sun_swing.solar_azimuth_at(self.utc_datetime)

    @property
    def angle_to_sun(self):
        return norm360(self.shadow_reading - self.sun_swing.pelorus_correction)

    @property
    def true_bearing(self):
        return norm360(360 - self.angle_to_sun + self.solar_azimuth)

    @property
    def magnetic_bearing(self):
        return norm360(self.true_bearing - self.sun_swing.variation)

    @property
    def deviation(self):
        deviation = norm360(self.magnetic_bearing - self.compass_reading)
        if deviation > 180:
            deviation = deviation - 360
        return deviation

    def __unicode__(self):
        return u"(%g, %g, %g)" % (self.video_time, self.compass_reading, self.shadow_reading)

    class Meta():
        ordering = ['video_time']
