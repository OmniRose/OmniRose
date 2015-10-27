import json
import pytz
from time import sleep
from datetime import datetime, timedelta
import re
import requests

from django.test import TestCase, Client
from omnirose.live_tests import OmniRoseSeleniumTestCase, LoginFailedException

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

from .models import Curve, Reading, ErrorNoSuitableEquationAvailable, mod360, SunSwingReading
from .equations import all_equations
from .samples import create_database_curve_from_sample, create_curve_calculation_from_sample, samples
from accounts.models import User


class CurveMathTests(TestCase):
    def test_mod360(self):
        self.assertEqual(mod360(0), 0)
        self.assertEqual(mod360(180), 180)
        self.assertEqual(mod360(359), 359)
        self.assertEqual(mod360(360), 0)
        self.assertEqual(mod360(370), 10)
        self.assertEqual(mod360(-10), 350)
        self.assertEqual(mod360(-12.34), 347.66)


class CurveBasicTests(TestCase):
    def test_unlocked(self):
        curve = Curve()

        # by default should not be paid
        self.assertEqual(curve.unlocked, None)
        self.assertFalse(curve.is_unlocked)

        # mark as paid, see what happens
        curve.set_unlocked_to_now()
        self.assertTrue(curve.is_unlocked)


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

    bearing_convert_test_values = (
        # (compass, true)
        (0, 356.157),
        (2, 358.299),
        (90, 93.843),
        (357, 352.949),
        (359, 355.087),
    )

    def test_compass_to_true(self):
        for compass, true in self.bearing_convert_test_values:
            self.assertAlmostEqual( self.curve.compass_to_true(compass), true)

        self.assertAlmostEqual( self.curve.compass_to_true(0, 10), 6.157)
        self.assertAlmostEqual( self.curve.compass_to_true(90, 10), 103.843)

    def test_true_to_compass(self):
        for compass, true in self.bearing_convert_test_values:
            self.assertAlmostEqual( self.curve.true_to_compass(true), compass)

        self.assertAlmostEqual( self.curve.true_to_compass(103.843, 10), 90)

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


class SunSwingTestsBase(object):
    fixtures = ['test_user_data']

    sun_swing_test_data = {
        # Real data from the first test swing of Olga
        "pelorus_correction": 156,
        "compass_video_start_time": 1444644781.875,
        # 2015-10-12 10:13:01.875000+00:00
        "latitude": 59.270133,
        "longitude": 18.790867,
        "readings": [
            { "compass": 20,    "shadow": 307.5,    "time": 70.6875   },
            { "compass": 30,    "shadow": 296,      "time": 74.9375   },
            { "compass": 40,    "shadow": 285.5,    "time": 78.46875  },
            { "compass": 50,    "shadow": 271,      "time": 83.46875  },
            { "compass": 60,    "shadow": 259,      "time": 87.75     },
            { "compass": 70,    "shadow": 246,      "time": 92.03125  },
            { "compass": 80,    "shadow": 235.5,    "time": 95.40625  },
            { "compass": 90,    "shadow": 224,      "time": 99.40625  },
            { "compass": 100,   "shadow": 213.5,    "time": 103.40625 },
            { "compass": 110,   "shadow": 203,      "time": 106.4375  },
            { "compass": 120,   "shadow": 191,      "time": 110.6875  },
            { "compass": 130,   "shadow": 179.5,    "time": 114.6875  },
            { "compass": 140,   "shadow": 168,      "time": 119.875   },
            { "compass": 150,   "shadow": 159.5,    "time": 122.5625  },
            { "compass": 160,   "shadow": 149,      "time": 126.9375  },
            { "compass": 170,   "shadow": 140.5,    "time": 129.78125 },
            { "compass": 180,   "shadow": 131,      "time": 133.625   },
            { "compass": 190,   "shadow": 124,      "time": 137.28125 },
            { "compass": 200,   "shadow": 115,      "time": 140.5625  },
            { "compass": 210,   "shadow": 104,      "time": 145.875   },
            { "compass": 220,   "shadow": 93,       "time": 151.15625 },
            { "compass": 230,   "shadow": 83,       "time": 156.28125 },
            { "compass": 240,   "shadow": 74.5,     "time": 161.09375 },
            { "compass": 250,   "shadow": 66,       "time": 165.46875 },
            { "compass": 260,   "shadow": 54,       "time": 170.71875 },
            { "compass": 280,   "shadow": 37.5,     "time": 177.84375 },
            { "compass": 290,   "shadow": 29.5,     "time": 181.53125 },
            { "compass": 300,   "shadow": 18,       "time": 186.375   },
            { "compass": 310,   "shadow": 10.5,     "time": 189.125   },
            { "compass": 320,   "shadow": 2,        "time": 192.625   },
            { "compass": 330,   "shadow": 354.5,    "time": 195.125   },
            { "compass": 340,   "shadow": 342.5,    "time": 198.96875 },
            { "compass": 350,   "shadow": 333.5,    "time": 202.78125 },
            { "compass": 0,     "shadow": 323,      "time": 206.5     },
            { "compass": 10,    "shadow": 312,      "time": 211.125   },
            { "compass": 20,    "shadow": 302.5,    "time": 215.28125 },
            { "compass": 30,    "shadow": 294,      "time": 218.25    },
        ]
    }

    def test_curve_and_readings(self):
        curve = self.curve
        test_data = self.sun_swing_test_data

        self.assertEqual(curve.reading_set.all().count(), len(test_data["readings"]))

        south_reading = curve.reading_set.filter(sunswingreading__compass_reading=180)[0]
        south = south_reading.sunswingreading

        # test against known good values
        self.assertAlmostEqual(south_reading.deviation, 14.616607)
        self.assertAlmostEqual(south_reading.ships_head, 194.616607)
        self.assertAlmostEqual(south.deviation, 14.616607)
        self.assertAlmostEqual(south.ships_head, 194.616607)

        self.assertEqual(south.utc_datetime, datetime(2015, 10, 12, 10, 15, 15, 500000, tzinfo=pytz.utc))
        self.assertEqual(south.variation, 6.02)
        self.assertAlmostEqual(south.solar_azimuth, 175.63660700)
        self.assertAlmostEqual(south.angle_to_sun, 335)
        self.assertAlmostEqual(south.true_bearing, 200.63660700)
        self.assertAlmostEqual(south.magnetic_bearing, 194.616607)
        self.assertAlmostEqual(south.calculated_deviation, 14.616607)


class SunSwingModelTests(SunSwingTestsBase, TestCase):
    def setUp(self):
        test_data = self.sun_swing_test_data

        curve = Curve.objects.create(
            user=User.objects.get(pk=1),
            vessel="Test",
            note="test",
        )

        start_utc_datetime = datetime.fromtimestamp(test_data["compass_video_start_time"], pytz.utc)

        latitude=test_data["latitude"]
        longitude=test_data["longitude"]

        pelorus_correction=test_data["pelorus_correction"]

        variation = 6.02 # declination(dlat=latitude, dlon=longitude, time=start_utc_datetime)

        for reading in test_data['readings']:
            sun_swing_reading = SunSwingReading(
                curve=curve,
                compass_reading=reading["compass"],
                shadow_reading=reading["shadow"],
                utc_datetime=start_utc_datetime + timedelta(seconds=reading["time"]),
                latitude=latitude,
                longitude=longitude,
                pelorus_correction=pelorus_correction,
            )

            sun_swing_reading.save()

        self.curve = curve


class SunSwingJsonPostTests(SunSwingTestsBase, TestCase):

    def setUp(self):
        c = Client()

        self.assertTrue(c.login(username="bob@test.com", password="secret"))

        self.response = c.post('/swing/sun_json/', content_type='application/json', data=json.dumps(test_data) )
        self.assertEqual(self.response.status_code, 200)

        self.curve = SunSwing.objects.all()[0]













class CurveLiveTests(OmniRoseSeleniumTestCase):

    fixtures = ['test_user_data', 'test_curve_data']

    def test_create_curve(self):
        sel = self.selenium

        # go to the create new curve page
        self.get_home()
        self.login()
        sel.find_element_by_link_text('Your deviation tables').click()
        sel.find_element_by_link_text('Add a new deviation table').click()

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
        curve_url = "http://localhost:8081/deviation_tables/" + str(curve.id) + "/"

        self.assertEqual(
            preview_image.get_attribute('src'),
            curve_url + "table_png/magnetic/?crop=1"
        )

        simpler_button.click()
        self.assertEqual(
            preview_image.get_attribute('src'),
            curve_url + "table_png/magnetic/?crop=1&equation=trig_5"
        )

        simpler_button.click()
        self.assertEqual(
            preview_image.get_attribute('src'),
            curve_url + "table_png/magnetic/?crop=1&equation=trig_3"
        )

        complex_button.click()
        self.assertEqual(
            preview_image.get_attribute('src'),
            curve_url + "table_png/magnetic/?crop=1&equation=trig_5"
        )

        choose_button.click()

        self.assertEqual(
            sel.current_url,
            curve_url
        )

        # Check that the curve's equation is correct. Reload curve first.
        curve = Curve.objects.get(id=curve.id)
        self.assertEqual(curve.equation_slug, "trig_5")

    def test_create_curve_having_account(self):
        sel = self.selenium

        # go to the create new curve page
        self.get_home()

        sel.find_element_by_partial_link_text('Read more').click()
        sel.find_element_by_link_text('Create your deviation table.').click()

        # check we are on the enter page
        self.assertRegexpMatches(sel.current_url, r'/accounts/enter/')

        # check that the info is displayed correctly
        self.assertRegexpMatches(
            sel.find_element_by_css_selector('div.alert-info').text,
            r'save the data and let you access it again'
        )

        # Login using form
        login = ActionChains(sel)
        login.send_keys('bob@test.com')
        login.send_keys(Keys.TAB)
        login.send_keys('secret')
        login.send_keys(Keys.RETURN)
        login.perform()

        # check we are on the create page
        self.assertRegexpMatches(sel.current_url, r'/deviation_tables/new/$')


    def test_create_curve_creating_account(self):
        sel = self.selenium

        # go to the create new curve page
        self.get_home()

        sel.find_element_by_partial_link_text('Read more').click()
        sel.find_element_by_link_text('Create your deviation table.').click()

        # check we are on the enter page
        self.assertRegexpMatches(sel.current_url, r'/accounts/enter/')

        # check that the info is displayed correctly
        self.assertRegexpMatches(
            sel.find_element_by_css_selector('div.alert-info').text,
            r'save the data and let you access it again'
        )

        # Focus on the create account form email field
        sel.find_element_by_css_selector('#register-form input[name=email]').click()

        # create account using form
        login = ActionChains(sel)
        login.send_keys('not-bob@test.com')
        login.send_keys(Keys.TAB)
        login.send_keys(Keys.RETURN)
        login.perform()

        # check we are on the create page
        self.assertRegexpMatches(sel.current_url, r'/deviation_tables/new/$')

        # Test that it also works when we enter an email address that can't be used.
        self.logout()

        self.get_home()

        sel.find_element_by_partial_link_text('Read more').click()
        sel.find_element_by_link_text('Create your deviation table.').click()

        # check we are on the enter page
        self.assertRegexpMatches(sel.current_url, r'/accounts/enter/')

        # check that the info is displayed correctly
        self.assertRegexpMatches(
            sel.find_element_by_css_selector('div.alert-info').text,
            r'save the data and let you access it again'
        )

        # Focus on the create account form email field
        sel.find_element_by_css_selector('#register-form input[name=email]').click()

        # create account using form but email that already exists
        login = ActionChains(sel)
        login.send_keys('not-bob@test.com')
        login.send_keys(Keys.TAB)
        login.send_keys(Keys.RETURN)
        login.perform()

        # check we are on the register page
        self.assertRegexpMatches(sel.current_url, r'/accounts/register/')

        # create account using form but email that already exists
        login = ActionChains(sel)
        login.send_keys('really-') # the "not-bob@test.com" is already in the field
        login.send_keys(Keys.TAB)
        login.send_keys(Keys.RETURN)
        login.perform()

        # check we are on the create page
        self.assertRegexpMatches(sel.current_url, r'/deviation_tables/new/$')

    def test_edit_curve_details(self):
        sel = self.selenium

        self.get_home()
        self.login()

        sel.find_element_by_link_text('Your deviation tables').click()
        sel.find_element_by_partial_link_text('Gypsy Moth').click()
        sel.find_element_by_id('curve_edit_link').click()

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
        sel.find_element_by_id('curve_edit_link').click()
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
        sel.find_element_by_link_text('Your deviation tables').click()
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

    def test_table_download_as_pdf(self):
        sel = self.selenium

        self.login('bob@test.com')
        sel.find_element_by_link_text('Your deviation tables').click()
        sel.find_element_by_partial_link_text('Gypsy Moth').click()

        pdf_url = sel.find_element_by_partial_link_text('Download table as PDF').get_attribute("href")
        # print pdf_url

        # check that we can't get PDF without cookie
        r = requests.get(pdf_url)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(
            r.url,
            self.live_server_url + '/accounts/login/'
        )

        # check that we can get the file with cookie
        sel_cookies = sel.get_cookie('sessionid')
        cookies = dict(sessionid=sel_cookies['value'])
        r = requests.get(pdf_url, cookies=cookies)

        self.assertEqual(r.url, pdf_url)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.headers['content-disposition'], "attachment; filename='gypsy-moth-table-magnetic.pdf'")
        self.assertEqual(r.headers['content-type'], 'application/pdf')

        # Final call from selenium so that the shutdown process goes smoothly
        self.get_home()


    def do_stripe_payment(self, card_name="good_visa", exp_mmyy="1234", cvc="123"):
        sel = self.selenium

        cards = {
            "good_visa": "4242424242424242",
            "decline_on_server": "4000000000000341",
        }
        card_number = cards[card_name]

        stripe_button = sel.find_element_by_css_selector("button.stripe-button-el")
        stripe_button.click()
        sleep(2)

        # See https://gist.github.com/josephmosby/ae7ca6d8128f02e306db for
        # useful code to copy

        sel.switch_to.frame('stripe_checkout_app')

        # Enter credit card number
        card_input = sel.find_element_by_css_selector('#card_number')
        for chunk in [card_number[x:x+4] for x in xrange(0,16,4)]:
            card_input.send_keys(chunk)
            sleep(0.25)

        # Enter expiry date
        exp_input = sel.find_element_by_css_selector('#cc-exp')
        for chunk in [exp_mmyy[x:x+2] for x in xrange(0,4,2)]:
            exp_input.send_keys(chunk)
            sleep(0.25)

        # Enter CVC check number
        csc_input = sel.find_element_by_css_selector('#cc-csc')
        csc_input.send_keys(cvc)

        submit_button = sel.find_element_by_css_selector('#submitButton')
        submit_button.click()

        # The part where we're redirected, sleep is here to allow the redirect
        # to catch up
        sel.switch_to_default_content()
        sleep(6)

        return None


    def test_curve_purchasing(self):
        sel = self.selenium

        self.get_home()

        # Log in as valid user, get url to the curve
        self.login('bob@test.com')
        sel.find_element_by_link_text('Your deviation tables').click()
        sel.find_element_by_partial_link_text('Gypsy Moth').click()
        sel.find_element_by_partial_link_text('Download rose as PDF(s)').click()

        # check that we are on purchase page
        self.assertRegexpMatches(sel.current_url, r'/unlock/$')

        # Check we stay on this page if declined
        self.do_stripe_payment("decline_on_server")
        self.assertRegexpMatches(sel.current_url, r'/unlock_failed/')
        self.assertEqual(sel.find_element_by_id('stripe_error_message').text, "Your card was declined.")

        # Check we stay on this page if declined
        sel.find_element_by_partial_link_text('Please try again').click()
        self.do_stripe_payment("good_visa")
        self.assertRegexpMatches(sel.current_url, r'/rose_select/$')






