from time import sleep
import re

from django.test import TestCase
from omnirose.live_tests import OmniRoseSeleniumTestCase, LoginFailedException

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

# Create your tests here.
from .models import Curve, Reading, ErrorNoSuitableEquationAvailable
from .equations import all_equations
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
        # curve with lots of points
        self.assertEqual(self.curve.choose_equation(), all_equations[0]['equation'])

        # curve with fewer points
        four_point_curve = self.create_curve('four_points')
        self.assertEqual(four_point_curve.choose_equation(), all_equations[5]['equation'])

        # No equation should match, raise exception
        too_few_points_curve = self.create_curve('too_few_points')
        self.assertRaises(ErrorNoSuitableEquationAvailable, too_few_points_curve.choose_equation)

    def test_suitable_equations_as_choices(self):
        self.assertEqual(
            self.curve.suitable_equations_as_choices(),
            [
                ('trig_13', '13 variable trig curve'),
                ('trig_11', '11 variable trig curve'),
                ('trig_9',  '9 variable trig curve'),
                ('trig_7',  '7 variable trig curve'),
                ('trig_5',  '5 variable trig curve'),
                ('trig_3',  '3 variable trig curve'),
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

        self.assertEqual(actual, samples['rya_training_almanac']['readings'])
        self.assertEqual(self.curve.readings_as_dict, samples['rya_training_almanac']['readings'])

    def test_choose_equation_database(self):
        expected = all_equations[0]['equation']
        self.assertEqual(self.curve.choose_equation(), expected)

        self.curve.equation_slug = 'trig_5'
        self.assertEqual(self.curve.choose_equation(), all_equations[4]['equation'])

        self.curve.equation_slug = 'does_not_exist'
        self.assertEqual(self.curve.choose_equation(), expected)

        # curve with fewer points
        four_point_curve = self.create_curve('four_points')
        self.assertEqual(four_point_curve.choose_equation(), all_equations[5]['equation'])

        # If given invalid equation still pick one that works
        four_point_curve.equation_slug = 'trig_5'
        self.assertEqual(four_point_curve.choose_equation(), all_equations[5]['equation'])


class DeviationCalculationTestCase(DeviationTestBase, TestCase):

    def create_curve(self, sample_name):
        return create_curve_calculation_from_sample(samples[sample_name])

    def test_readings_as_expected(self):
        """All reading included and correct accuracy"""
        self.assertEqual(self.curve.readings_as_dict, samples['rya_training_almanac']['readings'])




class CurveLiveTests(OmniRoseSeleniumTestCase):

    fixtures = ['test_user_data', 'test_curve_data']

    def test_create_curve(self):
        sel = self.selenium

        # go to the create new curve page
        self.get_home()
        self.login()
        sel.find_element_by_link_text('Your Curves').click()
        sel.find_element_by_link_text('Create a new curve').click()

        # Enter details
        vessel_input = sel.find_element_by_css_selector('input[name=vessel]')
        details = ActionChains(sel)
        details.move_to_element(vessel_input).click()
        details.send_keys('S/V Test Vessel')
        details.send_keys(Keys.TAB)
        details.send_keys('Starboard steering compass')
        details.send_keys(Keys.RETURN)
        details.perform()

        # Enter readings
        sleep(0.3)
        readings = ActionChains(sel)
        for deviation in (0, 2, 3, 2, 0, -2, -3, -2):
            readings.send_keys(str(deviation))
            readings.send_keys(Keys.TAB + Keys.TAB + Keys.TAB)
        readings.send_keys(Keys.RETURN)
        readings.perform()

        # Choose the equation
        sleep(0.3)
        simpler_button = sel.find_element_by_id("simpler_button")
        complex_button = sel.find_element_by_id("complex_button")
        choose_button = sel.find_element_by_id("choose_button")
        select_input = sel.find_element_by_css_selector("select")
        preview_image = sel.find_element_by_id("table_preview")

        curve = Curve.objects.all().order_by('created').last()
        curve_url = "http://localhost:8081/curves/" + str(curve.id) + "/"

        self.assertEqual(
            preview_image.get_attribute('src'),
            curve_url + "table_png/?crop=1"
        )

        simpler_button.click()
        self.assertEqual(
            preview_image.get_attribute('src'),
            curve_url + "table_png/?crop=1&equation=trig_5"
        )

        simpler_button.click()
        self.assertEqual(
            preview_image.get_attribute('src'),
            curve_url + "table_png/?crop=1&equation=trig_3"
        )

        complex_button.click()
        self.assertEqual(
            preview_image.get_attribute('src'),
            curve_url + "table_png/?crop=1&equation=trig_5"
        )

        choose_button.click()

        self.assertEqual(
            sel.current_url,
            curve_url
        )

        # Check that the curve's equation is correct. Reload curve first.
        curve = Curve.objects.get(id=curve.id)
        self.assertEqual(curve.equation_slug, "trig_5")

    def test_edit_curve_details(self):
        sel = self.selenium

        self.get_home()
        self.login()

        sel.find_element_by_link_text('Your Curves').click()
        sel.find_element_by_partial_link_text('Gypsy Moth').click()
        sel.find_element_by_link_text('edit').click()

        # update the values
        vessel_input = sel.find_element_by_css_selector('input[name=vessel]')
        vessel_input.clear()
        update = ActionChains(sel)
        update.move_to_element(vessel_input).click()
        update.send_keys("New Name")
        update.send_keys(Keys.TAB)
        update.send_keys("New Description")
        update.send_keys(Keys.RETURN)
        update.perform()

        # check values updated correctly
        sel.find_element_by_link_text('edit').click()
        self.assertEqual(
            sel.find_element_by_css_selector('input[name=vessel]').get_attribute("value"),
            "New Name"
        )
        self.assertEqual(
            sel.find_element_by_css_selector('input[name=note]').get_attribute("value"),
            "New Description"
        )

    def test_curve_permissions(self):
        sel = self.selenium

        self.get_home()

        # Log in as valid user, get url to the curve
        self.login('bob@test.com')
        sel.find_element_by_link_text('Your Curves').click()
        sel.find_element_by_partial_link_text('Gypsy Moth').click()
        curve_url = sel.current_url

        # Log out, test we can't see the curve page
        self.logout()
        sel.get(curve_url)
        self.assertNotEqual(curve_url, sel.current_url)
        self.assertEqual(sel.title, "Log in :: OmniRose")

        # Log in as another user, test we can't see the curve page
        self.login('notbob@test.com')
        sel.get(curve_url)
        self.assertNotEqual(curve_url, sel.current_url)
        self.assertEqual(sel.title, "Log in :: OmniRose")
