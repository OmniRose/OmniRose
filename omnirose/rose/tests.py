from django.test import TestCase
from .models import Rose
import os

from deviation.samples import create_curve_from_sample, rya_training_almanac

# Create your tests here.

class RoseTestCase(TestCase):
    def test_rose_creation(self):
        curve = create_curve_from_sample(rya_training_almanac)
        rose = Rose(variation=-6, deviation=curve)
        rose.draw_rose()
        os.rename(rose.filename, "rose_test.pdf")
        self.assertTrue(True)
