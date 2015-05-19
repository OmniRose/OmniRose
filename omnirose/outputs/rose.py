# coding=utf-8

import tempfile
import os
from math import sin, cos, radians, pi

import cairocffi as cairo

from omnirose.templatetags.omnirose_tags import east_west
from .base import OutputsTextMixin


class Rose(OutputsTextMixin):


    def __init__(self, variation, curve=None):
        self.SURFACE_HEIGHT = 790.
        self.SURFACE_WIDTH  = 590.

        self.edge_indent = 30.


        self.rose_centre_x = self.SURFACE_WIDTH / 2
        self.rose_centre_y = self.SURFACE_HEIGHT - self.rose_centre_x

        self.rose_width = 30.
        self.inter_rose_gap = 1.

        self.text_line_height = 1.2

        self.width_cardinal = 3 # N, S, E, W
        # self.width_ordinal  = 0.1 # NE, SW, SE, NE
        self.width_major    = 1
        self.width_minor    = 0.5
        self.width_tick     = 0.1

        (handle, cairo_tmp) = tempfile.mkstemp('.pdf', 'omnirose-rose')
        os.close(handle)
        self.filename = cairo_tmp

        self.surface = cairo.PDFSurface(self.filename, self.SURFACE_WIDTH, self.SURFACE_HEIGHT)
        self.context = cairo.Context(self.surface)
        self.variation = variation
        self.curve = curve


    def x_for_deg(self, deg, r):
        return self.rose_centre_x + r * sin(radians(deg))

    def y_for_deg(self, deg, r):
        return self.rose_centre_y - r * cos(radians(deg))


    def draw(self):

        outer_rose_radius = self.rose_centre_x - self.edge_indent
        inner_rose_radius = outer_rose_radius - self.rose_width - self.inter_rose_gap

        # Draw the true outer rose
        self.draw_ring(outer_rose_radius, self.rose_width, 'T', 0)

        # Draw the adjusted inner rose
        self.draw_ring(inner_rose_radius, self.rose_width, 'C', self.variation, self.curve)

        # Draw the variation
        self.draw_variation()

        # Draw the blurb
        self.draw_titles()



    def draw_ring(self, outer_radius, dist, superscript, variation=0, curve=None):
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

                    degree_text = unicode(display_degree)

                    degree_font_size = 8
                    degree_extra_spacing = 0.5 # so that the white background does not get too tight
                    superscript_font_size = 5

                    # size of degree numbers
                    context.set_font_size(degree_font_size)
                    (x_bearing, y_bearing, degree_width, degree_height, x_advance, y_advance) = context.text_extents(degree_text)

                    # size of superscript
                    context.set_font_size(superscript_font_size)
                    (x_bearing, y_bearing, superscript_width, superscript_height, x_advance, y_advance) = context.text_extents(superscript)

                    # size of them combined
                    width = degree_width + degree_extra_spacing + superscript_width
                    height = max(degree_height, superscript_height)

                    x = self.x_for_deg(plot_degree,mid_radius) - 0.5 * width
                    y = self.y_for_deg(plot_degree,mid_radius) + 0.5 * height

                    # Put a white rectangle behind the text to mask out lines
                    with context:
                        context.set_source_rgba(1, 1, 1, 1)  # White
                        context.rectangle(x-1, y+1, width+2, -height-2)
                        context.fill()

                    with context:
                        context.set_source_rgba(1, 0, 0, 1)  # Red

                        # Draw the degree text
                        context.move_to(x,y)
                        context.set_font_size(degree_font_size)
                        context.show_text(degree_text)

                        # Move the y position so that the top of text aligns
                        x,y = context.get_current_point()
                        y = y - height + superscript_height

                        # Draw the superscript
                        context.move_to(x,y)
                        context.set_font_size(superscript_font_size)
                        context.show_text(superscript)

    def draw_variation(self):
        var = self.variation

        text = east_west(var)

        with self.context as context:

            variation_font_size = 80
            copyright_font_size = 8

            context.set_source_rgb(0.6, 0.6, 0.6)  # gray
            context.set_font_size(variation_font_size)

            (x_bearing, y_bearing, width, height, x_advance, y_advance) = context.text_extents(text)

            x = self.rose_centre_x - 0.5 * width
            y = self.rose_centre_y + 0.5 * height

            context.move_to(x,y)
            context.show_text(text)

        with self.context as context:
            context.set_source_rgb(0.4, 0.4, 0.4)  # gray

            instructions = (
                "Outer ring: True",
                # "Middle ring: Magnetic",
                "Inner ring: Compass",
            )

            y = y + 4 * copyright_font_size

            for instruction in instructions:
                y = self.draw_text_block(
                    instruction,
                    copyright_font_size,
                    y,
                    max_width=300,
                    max_lines=8,
                )

        with self.context as context:
            context.set_source_rgb(0.4, 0.4, 0.4)  # gray
            y = y + 2 * copyright_font_size
            y = self.draw_text_block(self.copyright_string(), copyright_font_size, y)

