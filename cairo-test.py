# coding=utf-8

import cairocffi as cairo
from math import sin, cos, radians, pi

surface = cairo.PDFSurface('example.pdf', 500, 500)
# surface = cairo.SVGSurface('example.svg', 500, 500)
context = cairo.Context(surface)

with context:
    context.set_source_rgb(1, 1, 1)  # White
    context.paint()
# Restore the default source which is black.

def x_for_deg(deg, r):
    return 250 + r * sin(radians(deg))

def y_for_deg(deg, r):
    return 250 - r * cos(radians(deg))

def draw_rose(r, dist, deg_adjust=0):

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

draw_rose(200, 20, 0)
draw_rose(158, 20, 6)
