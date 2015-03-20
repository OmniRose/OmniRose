from django.test import TestCase
from .models import Table
import os

from deviation.samples import samples, create_curve_from_sample

# Create your tests here.

class TableTestCase(TestCase):
    def test_table_creation(self):
        for name, sample in samples.items():
            curve = create_curve_from_sample(sample)
            table = Table(curve=curve)
            table.draw()
            os.rename(table.filename, "test_output/table_%s.pdf" % name)
            self.assertTrue(True)
