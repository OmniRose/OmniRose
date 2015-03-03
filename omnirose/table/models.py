# coding=utf-8

import tempfile
import os
from math import sin, cos, radians, pi

import cairocffi as cairo

# This model does not persist to the database


class Table:


    def __init__(self, deviation=None):
        self.SURFACE_SIZE = 500

        self.grid_top    = 120
        self.grid_height = 360
        self.grid_width  = 200

        self.width_cardinal = 1 # N, S, E, W
        self.width_major    = 0.1
        self.width_minor    = 0.1
        self.width_tick     = 0

        (handle, cairo_tmp) = tempfile.mkstemp('.pdf', 'omnirose-table')
        os.close(handle)
        self.filename = cairo_tmp

        self.surface = cairo.PDFSurface(self.filename, self.SURFACE_SIZE, self.SURFACE_SIZE)
        self.context = cairo.Context(self.surface)
        self.deviation = deviation


    @property
    def grid_height_increment(self):
        return self.grid_height / 360

    def grid_y(self, degree):
        return self.grid_top + self.grid_height_increment * degree

    # def grid_x(self, deviation):
    #     return ????

    def draw_table(self):
        self.draw_degrees_grid()
        # self.draw_deviation_grid()
        # self.draw_readings()
        # self.draw_deviation_curve()

    def draw_degrees_grid(self):
        context = self.context

        midpoint = self.SURFACE_SIZE / 2
        x_start = midpoint - self.grid_width / 2
        x_end   = midpoint + self.grid_width / 2

        for degree in range(0, 361, 10):
            y = self.grid_y(degree)
            with context:
                if not degree % 90:
                    context.set_line_width(self.width_cardinal)
                elif not degree % 10:
                    context.set_line_width(self.width_major)
                elif not degree % 5:
                    context.set_line_width(self.width_minor)
                else:
                    context.set_line_width(self.width_tick)
                context.move_to(x_start, y)
                context.line_to(x_end, y)
                context.stroke()

            if not degree % 10:
                with context:
                    text = unicode(degree) + u'°'
                    context.set_font_size(6)

                    (x_bearing, y_bearing, width, height, x_advance, y_advance) = context.text_extents(text)

                    y = y + height / 2

                    for x in (x_start - width - 2, x_end + 2):
                        context.move_to(x,y)
                        context.show_text(text)



