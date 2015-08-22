# coding=utf-8

from datetime import datetime
from math import radians
from .helpers import split_into_lines

class OutputsTextMixin:

    def copyright_string(self):
        return u"© %s OmniRose.com" % (datetime.now().year)

    def draw_titles(self, initial_y=100):

        curve = self.curve

        y = initial_y
        y = self.draw_text_block(curve.vessel, 32, y, vertical_shift='text')
        y = self.draw_text_block(curve.note,   18, y, vertical_shift='text')


    def draw_text_block(self, text, font_size, y, max_lines=1, max_width=None, background_colour_rgba=None, vertical_shift='font'):
        context = self.context
        curve = self.curve

        if max_width is None:
            max_width = self.SURFACE_WIDTH - self.edge_indent

        with context:

            while font_size > 0:

                for line_count in range(1, max_lines+1):

                    lines = split_into_lines(text, line_count)

                    context.set_font_size(font_size)

                    largest_width = 0

                    for line in lines:
                        (x_bearing, y_bearing, width, height, x_advance, y_advance) = context.text_extents(line)
                        if width > largest_width:
                            largest_width = width

                    if largest_width < max_width:
                        break

                if largest_width < max_width:
                    break
                else:
                    font_size = font_size - 1

            fascent, fdescent, font_height, fxadvance, fyadvance = context.font_extents()

            for line in lines:
                (x_bearing, y_bearing, width, height, x_advance, y_advance) = context.text_extents(line)
                x = self.SURFACE_WIDTH/2 - width/2

                if background_colour_rgba:
                    padding = 2
                    context.set_source_rgba(*background_colour_rgba)
                    context.rectangle(x+x_bearing-padding, y+y_bearing-padding, width+2*padding, height+2*padding)
                    context.fill()
                    context.set_source_rgba(0,0,0,1)

                context.move_to(x,y)
                context.show_text(line)

                if vertical_shift == 'font':
                    y_delta = self.text_line_height * font_height
                elif vertical_shift == 'text':
                    y_delta = self.text_line_height * height
                else:
                    raise Exception("Bad parameter vertical_shift: %s" % vertical_shift)

                y = y + y_delta

        return y


    def get_text_width_height(self, text):
        return self.context.text_extents(text)[2:4]



    def produce_rotated_text(self, string, x, y, theta=0.0):
        # based on http://stackoverflow.com/a/17321410
        ctx = self.context

        fascent, fdescent, fheight, fxadvance, fyadvance = ctx.font_extents()
        x_off, y_off, tw, th = ctx.text_extents(string)[:4]

        nx = -tw/2.0
        ny = fheight/2.0

        ctx.translate(x,y)
        ctx.rotate(radians(theta))
        ctx.translate(nx, ny)
        ctx.move_to(0,0)
        ctx.show_text(string)


