
from .helpers import split_into_lines

class OutputsTextMixin:

    def draw_text(self):

        curve = self.curve

        y = 100
        y = self.draw_text_block(curve.vessel, 32, y)
        y = self.draw_text_block(curve.note, 18, y)


    def draw_text_block(self, text, font_size, y, max_lines=2):
        context = self.context
        curve = self.curve

        available_width = self.SURFACE_WIDTH - self.edge_indent

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

                    if largest_width < available_width:
                        break

                if largest_width < available_width:
                    break
                else:
                    font_size = font_size - 1





            for line in lines:
                (x_bearing, y_bearing, width, height, x_advance, y_advance) = context.text_extents(line)
                x = self.SURFACE_WIDTH/2 - width/2
                context.move_to(x,y)
                context.show_text(line)
                y = y + self.text_line_height * height

        return y
