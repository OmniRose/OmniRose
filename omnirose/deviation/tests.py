from django.test import TestCase

# Create your tests here.
from .models import Curve, Reading
from .samples import create_curve_from_sample, rya_training_almanac, instrument_flying_handbook

class DeviationTestCase(TestCase):

    def setUp(self):
        self.curve = create_curve_from_sample(rya_training_almanac)

    def test_readings_as_expected(self):
        """All reading included and correct accuracy"""
        actual = {}
        for reading in self.curve.reading_set.all():
            actual[reading.ships_head] = reading.deviation

        self.assertEqual(actual, rya_training_almanac)


    def test_curve_calculation(self):
        self.assertFalse(self.curve.curve_has_been_calculated())
        self.curve.calculate_curve()
        self.assertTrue(self.curve.curve_has_been_calculated())


    def test_calculated_deviation_as_expected(self):
        """Test that a deviation is calculated correctly"""
        self.assertEqual(self.curve.deviation_at(0), -3.964)
        self.assertEqual(self.curve.deviation_at(100), 4.593)

    def test_max_and_and_min_deviation_as_expected(self):
        self.assertEqual(self.curve.min_deviation, -6)
        self.assertEqual(self.curve.max_deviation, 6)

        handbook_curve = create_curve_from_sample(instrument_flying_handbook)
        self.assertEqual(handbook_curve.min_deviation, -5)
        self.assertEqual(handbook_curve.max_deviation, 6)


    def test_compass_to_true(self):
        self.assertEqual( self.curve.compass_to_true(90), 93.964)
        self.assertEqual( self.curve.compass_to_true(90, 10), 103.964)
