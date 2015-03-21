from django.db import models
from django.db.models import Max, Min
from django.core.urlresolvers import reverse

import warnings

import numpy
from scipy.optimize import curve_fit, OptimizeWarning

from accounts.models import User



# Curve equations - which one is used depends on the number of points available
# to plot to. There must be more points than there are variables.
def _raw_curve_equation_3(heading, A, B, C):
    return _raw_curve_equation_generic(heading, A, B, C)

def _raw_curve_equation_5(heading, A, B, C, D, E):
    return _raw_curve_equation_generic(heading, A, B, C, D, E)

def _raw_curve_equation_7(heading, A, B, C, D, E, F, G):
    return _raw_curve_equation_generic(heading, A, B, C, D, E, F, G)

def _raw_curve_equation_9(heading, A, B, C, D, E, F, G, H, I):
    return _raw_curve_equation_generic(heading, A, B, C, D, E, F, G, H, I)

def _raw_curve_equation_11(heading, A, B, C, D, E, F, G, H, I, J, K):
    return _raw_curve_equation_generic(heading, A, B, C, D, E, F, G, H, I, J, K)

def _raw_curve_equation_13(heading, A, B, C, D, E, F, G, H, I, J, K, L, M):
    return _raw_curve_equation_generic(heading, A, B, C, D, E, F, G, H, I, J, K, L, M)

def _raw_curve_equation_generic(heading, A, *args):
    heading_in_radians = numpy.radians(heading)

    result = A

    multiplier = 1

    while len(args):
        result = result + args[0] * numpy.sin(multiplier * heading_in_radians)
        result = result + args[1] * numpy.cos(multiplier * heading_in_radians)

        args = numpy.delete(args, [0,1])
        multiplier = multiplier + 1

    return result

_raw_curve_equations = (
    (13, _raw_curve_equation_13),
    (11, _raw_curve_equation_11),
    (9,  _raw_curve_equation_9),
    (7,  _raw_curve_equation_7),
    (5,  _raw_curve_equation_5),
    (3,  _raw_curve_equation_3),
)


class CurveCalculations(object):

    curve_equation = None

    curve_opt = None
    curve_cov = None

    _min_deviation = None
    _max_deviation = None

    _readings_as_dict = None

    @property
    def min_deviation(self):
        self._find_max_and_min_deviation_if_needed()
        return self._min_deviation

    @property
    def max_deviation(self):
        self._find_max_and_min_deviation_if_needed()
        return self._max_deviation


    def _find_max_and_min_deviation_if_needed(self):
        if self._min_deviation is not None and self._max_deviation is not None:
            return

        # Get the highest and lowest values from the readings as a starting
        # point
        deviations = self.readings_as_dict.values()
        min_dev = min(deviations)
        max_dev = max(deviations)

        # Would be nice to do this a little less brute forcish
        for degree in range(1, 360):
            dev = self.deviation_at(degree)
            if dev < min_dev: min_dev = dev
            if dev > max_dev: max_dev = dev

        self._min_deviation = int(numpy.floor(min_dev))
        self._max_deviation = int(numpy.ceil(max_dev))


    def deviation_at(self, heading):
        """Calculate the deviation for the given heading"""
        self.calculate_curve_if_needed()

        popt = self.curve_opt
        accurate = self.curve_equation(heading, *popt)
        return round(accurate, 3)


    def compass_to_true(self, compass, variation=0):
        magnetic = compass + self.deviation_at(compass)
        true = magnetic + variation
        return true


    # true_to_compass:
    #   note that this might be tricky to implement as second error correction
    #   will be needed.


    def calculate_curve_if_needed(self):
        if not self.curve_has_been_calculated():
            return self.calculate_curve()

    def curve_has_been_calculated(self):
        return bool(self.curve_opt is not None)

    @property
    def readings_as_dict(self):
        return self._readings_as_dict

    def calculate_curve(self):

        self._min_deviation = None
        self._max_deviation = None

        headings   = []
        deviations = []

        for ships_head, deviation in self.readings_as_dict.items():
            headings.append(ships_head)
            deviations.append(deviation)

        # Work out which equation to use
        for arg_count, equation in _raw_curve_equations:
            if len(headings) >= arg_count:
                break

        with warnings.catch_warnings():
            # We might get an "OptimizeWarning" that we want to ignore
            warnings.simplefilter("ignore", category=OptimizeWarning)
            popt, pcov = curve_fit(equation, numpy.array(headings), numpy.array(deviations))

        self.curve_equation = equation
        self.curve_opt = popt
        self.curve_cov = pcov


class Curve(CurveCalculations, models.Model):

    user   = models.ForeignKey(User, blank=True, null=True)
    vessel = models.CharField(max_length=80)
    note   = models.CharField(max_length=80)

    created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return u"%s (%s)" % (self.vessel, self.note)

    def get_absolute_url(self):
        return reverse('curve_detail', args=[str(self.id)])

    @property
    def readings_as_dict(self):
        readings = self.reading_set.all().order_by('ships_head')
        as_dict = {}
        for reading in readings:
            as_dict[reading.ships_head] = reading.deviation
        return as_dict


class Reading(models.Model):
    curve = models.ForeignKey(Curve)
    ships_head = models.FloatField()
    deviation = models.FloatField()

    class Meta():
        ordering = ['ships_head']

    def __unicode__(self):
        return "(%g, %g)" % (self.ships_head, self.deviation)



