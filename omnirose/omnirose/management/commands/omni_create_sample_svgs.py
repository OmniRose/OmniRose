from django.core.management.base import BaseCommand

import os
import sys
from subprocess import call

from outputs.models import Rose, Table
from curve.samples import create_database_curve_from_sample, samples


class Command(BaseCommand):
    help = 'generates the sample images in the static directory'


    def handle(self, *args, **options):
        sample = samples['rya_training_almanac']
        curve = create_database_curve_from_sample(sample)

        self.draw(Table(curve=curve), 'table')
        self.draw(Rose(curve=curve, variation=-7), 'rose')


    def draw(self, output, name):
        output.draw()
        output.surface.finish()

        destination = "omnirose/static/%s.svg" % name
        os.system('pdf2svg %s %s' % (output.filename, destination))
        os.remove(output.filename)

        self.stdout.write('Successfully generated %s' % name)
