from django.test import TestCase
from .models import Rose
import os

from deviation.samples import create_curve_from_sample, samples

# Create your tests here.

class RoseTestCase(TestCase):
    def test_rose_creation(self):
        for name, sample in samples.items():
            curve = create_curve_from_sample(sample)
            rose = Rose(variation=0, curve=curve)
            rose.draw()
            os.rename(rose.filename, "test_output/rose_%s.pdf" % name)
            self.assertTrue(True)
