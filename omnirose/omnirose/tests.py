# coding=utf-8

from django.test import TestCase
from django.template import Template, Context

from .templatetags.omnirose_tags import east_west

class EastWestTagTest(TestCase):

    TEMPLATE = Template("{% load omnirose_tags %}{{ degrees|east_west }}")

    TEST_VALUES = {
        -1.5: u"1.5°W",
        -1:   u"1°W",
        0:    u"0°",
        0.00: u"0°",
        1:    u"1°E",
        1.5:  u"1.5°E",
        123.456789: u"123.457°E",
    }

    def test_template_tag(self):
        for degrees, expected in self.TEST_VALUES.items():
            rendered = self.TEMPLATE.render(Context({"degrees": degrees}))
            self.assertEqual(expected, rendered)

    def test_function_directly(self):
        for degrees, expected in self.TEST_VALUES.items():
            rendered = east_west(degrees)
            self.assertEqual(expected, rendered)
