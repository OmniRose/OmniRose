from django.test import TestCase
from .models import Table
import os

from deviation.samples import samples, create_curve_from_sample

# Create your tests here.

class TableTestCase(TestCase):
    def test_table_creation(self):
        curve = create_curve_from_sample(samples['rya_training_almanac'])
        table = Table(curve=curve)
        table.draw()
        os.rename(table.filename, "table_test.pdf")
        self.assertTrue(True)
