import textwrap


def short_text(text, width=30):
    return textwrap.shorten(text, width=width)
