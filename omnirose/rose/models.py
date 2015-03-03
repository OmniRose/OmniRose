# coding=utf-8

from math import sin, cos, radians, pi

# This model does not persist to the database

def x_for_deg(deg, r):
    return 250 + r * sin(radians(deg))

def y_for_deg(deg, r):
    return 250 - r * cos(radians(deg))

class Rose:
    def __init__(self, context, variation):
        self.context = context
        self.variation = variation


    def draw_rose(self):
        self.draw_one_rose(200, 20, 0)
        self.draw_one_rose(158, 20, self.variation)


    def draw_one_rose(self, r, dist, deg_adjust=0):
        context = self.context


        for deg in range(0, 360):

            rose_width = dist

            with context:
                if not deg % 90:
                    context.set_line_width(2.5)
                elif not deg % 10:
                    context.set_line_width(1)
                elif not deg % 5:
                    context.set_line_width(0.5)
                else:
                    context.set_line_width(0.1)
                    # rose_width = dist - 1

                context.move_to(x_for_deg(deg+deg_adjust,r-rose_width),y_for_deg(deg+deg_adjust,r-rose_width))
                context.line_to(x_for_deg(deg+deg_adjust,r+rose_width),y_for_deg(deg+deg_adjust,r+rose_width))
                context.stroke()

        for deg in range(0, 360):
            if not deg % 10:
                with context:
                    text = unicode(deg) + u'°'

                    context.set_font_size(8)
                    # context.rotate(rad - 0.5 * pi)

                    (x_bearing, y_bearing, width, height, x_advance, y_advance) = context.text_extents(text)
                    print x_bearing, y_bearing, width, height, x_advance, y_advance

                    x = x_for_deg(deg+deg_adjust,r) - 0.5 * width
                    y = y_for_deg(deg+deg_adjust,r) + 0.5 * height

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


