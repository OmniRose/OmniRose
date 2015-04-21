def split_into_lines(text, line_count):

    lines = []
    line_length = len(text) / line_count

    words = text.split()
    line = []

    for word in words:
        line.append(word)
        line_as_text = " ".join(line)
        if len(line_as_text) >= line_length:
            lines.append(line_as_text)
            line = []

    line_as_text = " ".join(line)
    if len(line_as_text):
        lines.append(line_as_text)

    return lines
