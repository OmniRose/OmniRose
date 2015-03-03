# coding=utf-8

import tempfile
import os
from math import sin, cos, radians, pi

import cairocffi as cairo

# This model does not persist to the database


class Rose:


    def __init__(self, variation, curve=None):
        self.SURFACE_SIZE = 500.
        self.rose_width = 30.
        self.inter_rose_gap = 1.
        self.edge_indent = 10.

        self.width_cardinal = 3 # N, S, E, W
        # self.width_ordinal  = 0.1 # NE, SW, SE, NE
        self.width_major    = 1
        self.width_minor    = 0.5
        self.width_tick     = 0.1

        (handle, cairo_tmp) = tempfile.mkstemp('.pdf', 'omnirose-rose')
        os.close(handle)
        self.filename = cairo_tmp

        self.surface = cairo.PDFSurface(self.filename, self.SURFACE_SIZE, self.SURFACE_SIZE)
        self.context = cairo.Context(self.surface)
        self.variation = variation
        self.curve = curve


    def x_for_deg(self, deg, r):
        return self.SURFACE_SIZE / 2 + r * sin(radians(deg))

    def y_for_deg(self, deg, r):
        return self.SURFACE_SIZE / 2 - r * cos(radians(deg))


    def draw_rose(self):

        outer_rose_radius = self.SURFACE_SIZE / 2 - self.edge_indent
        inner_rose_radius = outer_rose_radius - self.rose_width - self.inter_rose_gap

        # Draw the true outer rose
        self.draw_ring(outer_rose_radius, self.rose_width, 0)

        # Draw the adjusted inner rose
        self.draw_ring(inner_rose_radius, self.rose_width, self.variation, self.curve)


    def draw_ring(self, outer_radius, dist, variation=0, curve=None):
        context = self.context

        inner_radius = outer_radius - dist
        mid_radius = (inner_radius + outer_radius) / 2


        for display_degree in range(0, 360):

            if curve:
                plot_degree = curve.compass_to_true(display_degree, variation)
            else:
                plot_degree = display_degree + variation

            with context:
                if not display_degree % 90:
                    context.set_line_width(self.width_cardinal)
                elif not display_degree % 10:
                    context.set_line_width(self.width_major)
                elif not display_degree % 5:
                    context.set_line_width(self.width_minor)
                else:
                    context.set_line_width(self.width_tick)

                start_x = self.x_for_deg(plot_degree, inner_radius)
                start_y = self.y_for_deg(plot_degree, inner_radius)
                end_x   = self.x_for_deg(plot_degree, outer_radius)
                end_y   = self.y_for_deg(plot_degree, outer_radius)

                context.move_to(start_x, start_y)
                context.line_to(end_x, end_y)
                context.stroke()

        for display_degree in range(0, 360):

            if curve:
                plot_degree = curve.compass_to_true(display_degree, variation)
            else:
                plot_degree = display_degree + variation

            if not display_degree % 10:
                with context:
                    text = unicode(display_degree) + u'°'

                    context.set_font_size(8)
                    # context.rotate(rad - 0.5 * pi)

                    (x_bearing, y_bearing, width, height, x_advance, y_advance) = context.text_extents(text)

                    x = self.x_for_deg(plot_degree,mid_radius) - 0.5 * width
                    y = self.y_for_deg(plot_degree,mid_radius) + 0.5 * height

                    # Put a white rectangle behind the text to mask out lines
                    with context:
                        context.set_source_rgba(1, 1, 1, 1)  # White
                        context.rectangle(x-1, y+1, width+2, -height-2)
                        # context.rectangle(x, y, width, -height)
                        context.fill()

                        # dd = 0.4
                        # for dx in (-dd, dd):
                        #     for dy in (-dd, dd):
                        #             context.move_to(x + dx, y + dy)
                        #             context.show_text(text)

                    with context:
                        context.set_source_rgba(1, 0, 0, 1)  # Red
                        context.move_to(x,y)
                        # context.rotate(radians(deg))
                        context.show_text(text)


