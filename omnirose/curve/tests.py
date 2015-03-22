from django.test import TestCase

# Create your tests here.
from .models import Curve, Reading, ErrorNoSuitableEquationAvailable
from .samples import create_database_curve_from_sample, create_curve_calculation_from_sample, samples

class DeviationTestBase(object):

    def setUp(self):
        self.curve = self.create_curve('rya_training_almanac')

    def test_curve_calculation(self):
        self.assertFalse(self.curve.curve_has_been_calculated())
        self.curve.calculate_curve()
        self.assertTrue(self.curve.curve_has_been_calculated())


    def test_calculated_deviation_as_expected(self):
        """Test that a deviation is calculated correctly"""
        self.assertEqual(self.curve.deviation_at(0), -3.843)
        self.assertEqual(self.curve.deviation_at(100), 4.509)

    def test_max_and_and_min_deviation_as_expected(self):
        self.assertEqual(self.curve.min_deviation, -7)
        self.assertEqual(self.curve.max_deviation, 7)

        handbook_curve = self.create_curve('instrument_flying_handbook')
        self.assertEqual(handbook_curve.min_deviation, -7)
        self.assertEqual(handbook_curve.max_deviation, 6)


    def test_compass_to_true(self):
        self.assertEqual( self.curve.compass_to_true(90), 93.843)
        self.assertEqual( self.curve.compass_to_true(90, 10), 103.843)

    def test_can_calculate_curve(self):
        self.assertTrue(self.curve.can_calculate_curve)

        too_few_points_curve = self.create_curve('too_few_points')
        self.assertFalse(too_few_points_curve.can_calculate_curve)

    def test_choose_equation(self):
        self.assertTrue(self.curve.choose_equation())

        too_few_points_curve = self.create_curve('too_few_points')
        self.assertRaises(ErrorNoSuitableEquationAvailable, too_few_points_curve.choose_equation)

    def test_suitable_equations_as_choices(self):
        self.assertEqual(
            self.curve.suitable_equations_as_choices(),
            [
                ('trig_13', '13 variable trig curve'),
                ('trig_13', '11 variable trig curve'),
                ('trig_13', '9 variable trig curve'),
                ('trig_13', '7 variable trig curve'),
                ('trig_13', '5 variable trig curve'),
                ('trig_13', '3 variable trig curve'),
            ]
        )

        too_few_points_curve = self.create_curve('too_few_points')
        self.assertEqual(
            too_few_points_curve.suitable_equations_as_choices(),
            []
        )


class DeviationDatabaseTestCase(DeviationTestBase, TestCase):

    def create_curve(self, sample_name):
        return create_database_curve_from_sample(samples[sample_name])

    def test_readings_as_expected(self):
        """All reading included and correct accuracy"""
        actual = {}
        for reading in self.curve.reading_set.all():
            actual[reading.ships_head] = reading.deviation

        self.assertEqual(actual, samples['rya_training_almanac'])
        self.assertEqual(self.curve.readings_as_dict, samples['rya_training_almanac'])

class DeviationCalculationTestCase(DeviationTestBase, TestCase):

    def create_curve(self, sample_name):
        return create_curve_calculation_from_sample(samples[sample_name])

    def test_readings_as_expected(self):
        """All reading included and correct accuracy"""
        self.assertEqual(self.curve.readings_as_dict, samples['rya_training_almanac'])
