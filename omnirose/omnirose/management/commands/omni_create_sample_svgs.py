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

        self.draw(Table(curve=curve), 'table', x=150, y=540)
        self.draw(Rose(curve=curve, variation=-7), 'rose', x=269, y=520)



    def draw(self, output, name, x, y, height=200, width=200):

        static_dir = "static/"

        output.draw()
        output.surface.finish()

        destination_svg = static_dir + "%s.svg" % name

        os.system('pdf2svg %s %s' % (output.filename, destination_svg))
        os.remove(output.filename)

        destination_png     = static_dir + "%s.png" % name
        destination_cropped = static_dir + "%s_cropped.png" % name

        inkscape_cmd = "inkscape %s --without-gui --export-dpi=180" % destination_svg
        os.system(inkscape_cmd + " -e %s" % destination_png)
        os.system(inkscape_cmd + " -e %s --export-area=%u:%u:%u:%u" % (destination_cropped, x, y, x + width, y + height))

        for file in destination_png, destination_cropped:
            os.system("optipng %s" % file)

        self.stdout.write('Successfully generated %s' % name)
