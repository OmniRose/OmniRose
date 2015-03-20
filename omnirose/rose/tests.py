from django.test import TestCase
from .models import Rose
import os

from deviation.samples import create_curve_from_sample, samples

# Create your tests here.

class RoseTestCase(TestCase):
    def test_rose_creation(self):
        curve = create_curve_from_sample(samples['rya_training_almanac'])
        rose = Rose(variation=-6, curve=curve)
        rose.draw()
        os.rename(rose.filename, "rose_test.pdf")
        self.assertTrue(True)
