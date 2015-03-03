from django.test import TestCase
from .models import Table
import os

from deviation.samples import create_curve_from_sample, rya_training_almanac

# Create your tests here.

class TableTestCase(TestCase):
    def test_table_creation(self):
        curve = create_curve_from_sample(rya_training_almanac)
        table = Table(curve=curve)
        table.draw_table()
        os.rename(table.filename, "table_test.pdf")
        self.assertTrue(True)
