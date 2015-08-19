from django.test import TestCase
import os

from .models import Rose, Table
from .helpers import split_into_lines
from curve.samples import create_database_curve_from_sample, samples

class RoseTestCase(TestCase):
    def test_rose_creation(self):
        for name, sample in samples.items():
            curve = create_database_curve_from_sample(sample)

            if not curve.can_calculate_curve:
                continue

            rose = Rose(variation=0, curve=curve)
            rose.draw()
            os.rename(rose.filename, "test_output/rose_%s.pdf" % name)
            self.assertTrue(True)

    def test_multiple_rose_creation(self):
        name = 'rya_training_almanac'
        sample = samples[name]

        curve = create_database_curve_from_sample(sample)

        rose = Rose(variation=-1, variation_max=1, curve=curve)
        rose.draw()
        os.rename(rose.filename, "test_output/rose_%s_multiple.pdf" % name)
        self.assertTrue(True)


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


    def test_split_lines(self):
        text = "Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor"

        self.assertEqual(
            split_into_lines(text, 1),
            [
                "Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor",
            ]
        )
        self.assertEqual(
            split_into_lines(text, 2),
            [
                "Lorem ipsum dolor sit amet, consectetur",
                "adipisicing elit, sed do eiusmod tempor",
            ]
        )
        self.assertEqual(
            split_into_lines(text, 3),
            [
                "Lorem ipsum dolor sit amet,",
                "consectetur adipisicing elit,",
                "sed do eiusmod tempor",
            ]
        )
