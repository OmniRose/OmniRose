from django.db import models


class Curve(models.Model):

    def __unicode__(self):
        return unicode(self.id)

class Reading(models.Model):
    curve = models.ForeignKey(Curve)
    ships_head = models.FloatField()
    deviation = models.FloatField()

    def __unicode__(self):
        return "(%.1f, %.1f)" % (self.ships_head, self.deviation)
