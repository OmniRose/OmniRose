# coding=utf-8

import tempfile
import os
from math import sin, cos, radians, pi

import cairocffi as cairo

from omnirose.templatetags.omnirose_tags import east_west
from .base import OutputsTextMixin


class Rose(OutputsTextMixin):


    def __init__(self, variation, variation_max=None, curve=None):
        self.SURFACE_HEIGHT = 790.
        self.SURFACE_WIDTH  = 590.

        self.edge_indent = 30.


        self.rose_centre_x = self.SURFACE_WIDTH / 2
        self.rose_centre_y = self.SURFACE_HEIGHT - self.rose_centre_x

        self.rose_width = 30.
        self.inter_rose_gap = 2.

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
        self.curve = curve

        self.variation = variation

        if variation_max is None:
            self.variation_max = variation
        else:
            self.variation_max = variation_max

        self.magnetic_background_colour_rgba  = (1, 0.95, 0.95, 1)
        self.magnetic_text_colour_rgba = (0.2, 0, 0, 1)

        self.true_background_colour_rgba = (0.95, 1, 0.95, 1)
        self.true_text_colour_rgba = (0, 0.2, 0, 1)

        self.compass_background_colour_rgba = (0.95, 0.95, 1, 1)
        self.compass_text_colour_rgba = (0, 0, 0.2, 1)



    def x_for_deg(self, deg, r):
        return self.rose_centre_x + r * sin(radians(deg))

    def y_for_deg(self, deg, r):
        return self.rose_centre_y - r * cos(radians(deg))


    def draw(self):
        page_number = 0
        for variation in range(self.variation, self.variation_max + 1):

            # We need to start on a new page if this is not the first page.
            if page_number > 0:
                self.surface.show_page()
            page_number = page_number + 1

            self.draw_page(variation)

    def draw_page(self, variation):
        magnetic_rose_width = self.rose_width * 1
        true_rose_width     = self.rose_width * 1.2
        compass_rose_width  = self.rose_width * 1

        magnetic_rose_radius = self.rose_centre_x - self.edge_indent
        true_rose_radius = magnetic_rose_radius - magnetic_rose_width - self.inter_rose_gap
        compass_rose_radius = true_rose_radius - true_rose_width - self.inter_rose_gap


        # Draw the magnetic rose
        self.draw_ring(
            magnetic_rose_radius, magnetic_rose_width, 'M', variation, None,
            background_colour_rgba=self.magnetic_background_colour_rgba,
            text_colour_rgba=self.magnetic_text_colour_rgba,
        )

        # Draw the true rose
        self.draw_ring(
            true_rose_radius, true_rose_width, 'T', 0, None,
            background_colour_rgba=self.true_background_colour_rgba,
            text_colour_rgba=self.true_text_colour_rgba,
        )

        # Draw the adjusted compass rose
        self.draw_ring(
            compass_rose_radius, compass_rose_width, 'C', variation, self.curve,
            background_colour_rgba=self.compass_background_colour_rgba,
            text_colour_rgba=self.compass_text_colour_rgba,
        )

        # Draw the variation
        self.draw_variation(variation)

        # Draw the blurb
        self.draw_titles()



    def draw_ring(self, outer_radius, dist, superscript, variation, curve, background_colour_rgba, text_colour_rgba):
        context = self.context

        inner_radius = outer_radius - dist
        mid_radius = (inner_radius + outer_radius) / 2


        # draw background colour for the ring
        with context:
            context.new_path()
            context.set_source_rgba(*background_colour_rgba)
            context.set_line_width(dist)
            context.arc(self.rose_centre_x, self.rose_centre_y, mid_radius, 0, 2*pi)
            context.stroke()

        for display_degree in range(0, 360):

            if curve:
                plot_degree = curve.compass_to_true(display_degree, variation)
            else:
                plot_degree = display_degree + variation

            with context:

                context.set_source_rgba(0,0,0,1)

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

                    degree_font_size = 9
                    degree_extra_spacing = 1 # so that the white background does not get too tight
                    superscript_font_size = 6

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
                        context.set_source_rgba(*background_colour_rgba)  # White
                        context.rectangle(x-1, y+1, width+2, -height-2)
                        context.fill()

                    with context:
                        context.set_source_rgba(*text_colour_rgba)

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

    def draw_variation(self, var):

        text = east_west(var)

        with self.context as context:

            variation_font_size = 80
            legend_font_size = 12
            copyright_font_size = 12

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
                ("Magnetic bearings",self.magnetic_background_colour_rgba),
                ("True bearings",     self.true_background_colour_rgba),
                ("Compass bearings",  self.compass_background_colour_rgba),
            )

            y = y + 2 * legend_font_size

            for instruction, background_colour_rgba in instructions:
                y = self.draw_text_block(
                    instruction,
                    legend_font_size,
                    y + 4,
                    max_width=300,
                    max_lines=1,
                    background_colour_rgba=background_colour_rgba,
                )

        with self.context as context:
            context.set_source_rgb(0.4, 0.4, 0.4)  # gray
            y = y + 2 * copyright_font_size
            y = self.draw_text_block(self.copyright_string(), copyright_font_size, y)

