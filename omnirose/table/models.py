# coding=utf-8

import tempfile
import os
from math import sin, cos, radians, pi

import cairocffi as cairo

# This model does not persist to the database


class Table:


    def __init__(self, deviation=None):
        self.SURFACE_SIZE = 500.

        self.grid_top    = 120.
        self.grid_height = 360.
        self.grid_width  = 200.
        self.grid_bleed  = 2.

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
    def grid_content_height(self):
        return self.grid_height - self.grid_bleed * 2

    @property
    def grid_bottom(self):
        return self.grid_top + self.grid_height

    @property
    def grid_content_top(self):
        return self.grid_top + self.grid_bleed

    @property
    def grid_content_bottom(self):
        return self.grid_content_top + self.grid_content_height

    @property
    def grid_left(self):
        return self.SURFACE_SIZE / 2 - self.grid_width / 2

    @property
    def grid_right(self):
        return self.SURFACE_SIZE / 2 + self.grid_width / 2

    @property
    def grid_content_left(self):
        return self.grid_left + self.grid_bleed

    @property
    def grid_content_right(self):
        return self.grid_right - self.grid_bleed


    @property
    def grid_height_increment(self):
        return self.grid_content_height / 360

    def grid_y(self, degree):
        return self.grid_content_top + self.grid_height_increment * degree

    def grid_x(self, deviation):
        min_dev = self.deviation.min_deviation
        max_dev = self.deviation.max_deviation
        spread = max_dev - min_dev
        dev_interval = (self.grid_content_right - self.grid_content_left) / spread

        return self.grid_content_right - dev_interval * (max_dev - deviation)

    def draw_table(self):
        self.draw_degrees_grid()
        self.draw_deviation_grid()
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




    def draw_deviation_grid(self):
        context = self.context

        min_dev = self.deviation.min_deviation
        max_dev = self.deviation.max_deviation

        for dev in range(min_dev, max_dev + 1):

            x = self.grid_x(dev)

            y_start = self.grid_top
            y_end   = self.grid_bottom


            with context:
                if dev == 0:
                    context.set_line_width(self.width_cardinal)
                else:
                    context.set_line_width(self.width_major)
                context.move_to(x, y_start)
                context.line_to(x, y_end)
                context.stroke()

                text = unicode(dev) + u'°'
                context.set_font_size(6)

                (x_bearing, y_bearing, width, height, x_advance, y_advance) = context.text_extents(text)

                x = x - width/2

                for y in (y_start - height, y_end + height + 2):
                    context.move_to(x,y)
                    context.show_text(text)
