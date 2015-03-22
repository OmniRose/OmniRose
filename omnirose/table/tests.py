from django.test import TestCase
from .models import Table
import os

from curve.samples import samples, create_database_curve_from_sample

# Create your tests here.

class TableTestCase(TestCase):
    def test_table_creation(self):
        for name, sample in samples.items():
            curve = create_database_curve_from_sample(sample)

            if not curve.can_calculate_curve:
                continue

            table = Table(curve=curve)
            table.draw()
            os.rename(table.filename, "test_output/table_%s.pdf" % name)
            self.assertTrue(True)
