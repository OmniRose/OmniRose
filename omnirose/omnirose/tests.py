# coding=utf-8

from time import sleep

from django.test import TestCase
from django.template import Template, Context

from .templatetags.omnirose_tags import east_west
from omnirose.live_tests import OmniRoseSeleniumTestCase

class EastWestTagTest(TestCase):

    TEMPLATE = Template("{% load omnirose_tags %}{{ degrees|east_west }}")
    TEMPLATE_FLOAT = Template("{% load omnirose_tags %}{{ degrees|floatformat|east_west }}")

    TEST_BOTH = (
        (-1.5, u"1.5°W"),
        (-1,   u"1°W"),
        (0,    u"0°"),
        (1,    u"1°E"),
        (1.5,  u"1.5°E"),
    )

    TEST_VALUES = (
        (123.456789, u"123.457°E"),
    )

    TEST_VALUES_FLOAT = (
        (123.456789, u"123.5°E"),
    )

    def values_test(self, values, template):
        for degrees, expected in values:
            rendered = template.render(Context({"degrees": degrees}))
            self.assertEqual(expected, rendered)

    def test_template_tag(self):
        self.values_test(self.TEST_BOTH, self.TEMPLATE)
        self.values_test(self.TEST_BOTH, self.TEMPLATE_FLOAT)
        self.values_test(self.TEST_VALUES,       self.TEMPLATE)
        self.values_test(self.TEST_VALUES_FLOAT, self.TEMPLATE_FLOAT)

    def test_function_directly(self):
        for degrees, expected in self.TEST_VALUES:
            rendered = east_west(degrees)
            self.assertEqual(expected, rendered)


class ErrorPagesTest(OmniRoseSeleniumTestCase):
    def test_404_pages(self):
        sel = self.selenium

        self.get_home()
        sel.get(sel.current_url + "not/a/page")

        self.assertEqual(sel.title, "404 Page not found :: OmniRose")
