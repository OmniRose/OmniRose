from django.db import models

import numpy
from scipy.optimize import curve_fit


def _raw_curve_equation(heading, A, B, C, D, E):
    heading_in_radians = numpy.radians(heading)

    B_result = B * numpy.sin(heading_in_radians)
    C_result = C * numpy.cos(heading_in_radians)
    D_result = D * numpy.sin(2 * heading_in_radians)
    E_result = E * numpy.cos(2 * heading_in_radians)

    return A + B_result + C_result + D_result + E_result

class Curve(models.Model):

    curve_opt = None
    curve_cov = None

    def __unicode__(self):
        return unicode(self.id)


    def deviation_at(self, heading):
        """Calculate the deviation for the given heading"""
        if not self.curve_has_been_calculated():
            self.calculate_curve()

        popt = self.curve_opt
        accurate = _raw_curve_equation(heading, *popt)
        return round(accurate, 3)


    def curve_has_been_calculated(self):
        return bool(self.curve_opt is not None)


    def calculate_curve(self):

        headings   = []
        deviations = []

        readings = self.reading_set.all().order_by('ships_head')
        for reading in readings:
            headings.append(reading.ships_head)
            deviations.append(reading.deviation)

        popt, pcov = curve_fit(_raw_curve_equation, numpy.array(headings), numpy.array(deviations))

        self.curve_opt = popt
        self.curve_cov = pcov


class Reading(models.Model):
    curve = models.ForeignKey(Curve)
    ships_head = models.FloatField()
    deviation = models.FloatField()

    def __unicode__(self):
        return "(%.1f, %.1f)" % (self.ships_head, self.deviation)
