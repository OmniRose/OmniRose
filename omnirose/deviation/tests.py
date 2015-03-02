from django.test import TestCase

# Create your tests here.
from .models import Curve, Reading

# Create a test curve using RYA Training Almanac.
training_almanac_readings = {
    0    : -4,
    22.5 : -2,
    45   :  0,
    67.5 :  2,
    90   :  4,
    112.5:  5,
    135  :  6,
    157.5:  5,
    180  :  4,
    202.5:  2,
    225  :  0,
    247.5: -2,
    270  : -4,
    292.5: -5,
    315  : -6,
    337.5: -5,
}

class AnimalTestCase(TestCase):
    def setUp(self):
        self.curve = Curve.objects.create()
        for ships_head, deviation in training_almanac_readings.items():
            self.curve.reading_set.create(ships_head=ships_head, deviation=deviation)


    def test_readings_as_expected(self):
        """All reading included and correct accuracy"""
        actual = {}
        for reading in self.curve.reading_set.all():
            actual[reading.ships_head] = reading.deviation

        self.assertEqual(actual, training_almanac_readings)
