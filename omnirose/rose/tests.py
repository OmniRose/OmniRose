from django.test import TestCase
from .models import Rose

import cairocffi as cairo

# Create your tests here.

surface = cairo.PDFSurface('rose_test.pdf', 500, 500)



context = cairo.Context(surface)

rose = Rose(context, 6)
rose.draw_rose()
