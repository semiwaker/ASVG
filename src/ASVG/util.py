from ASVG.core import *
from ASVG.basicElements import *
from ASVG.text import *


def labeledRect(
        level: int,
        width: float,
        height: float,
        s: Union[str, TextRepresent],
        font_size: float,
        textShift: Tuple[float, float] = (0, 0),
        font: str = "Arial",
        rx: float = 0,
        ry: float = 0,
        margin: float = 5,
        attrib: Attrib = Attrib(),
        rectAttrib: Attrib = Attrib(),
        textAttrib: Attrib = Attrib(),
        **kwargs):
    e = ComposedElement((width + 2 * margin, height + 2 * margin),
                        level, attrib + kwargs)
    rect(e, 0, margin, margin, width, height, rx, ry, attrib=rectAttrib)

    textX = width / 2 + textShift[0] + margin
    textY = height / 2 + textShift[1] + (font_size / 2) + margin
    text(e, 1, s, textX, textY, font_size, font, attrib=textAttrib)
    return e


def labeledCircle(
        level: int,
        r: float,
        s: Union[str, TextRepresent],
        font_size: float,
        textShift: Tuple[float, float] = (0, 0),
        font: str = "Arial",
        margin: float = 5,
        attrib: Attrib = Attrib(),
        circleAttrib: Attrib = Attrib(),
        textAttrib: Attrib = Attrib(),
        **kwargs):
    e = ComposedElement((2 * (margin + r), 2 * (margin + r)),
                        level, attrib + kwargs)
    circle(e, 0, margin + r, margin + r, r, attrib=circleAttrib)

    textX = r + textShift[0] + margin
    textY = r + textShift[1] + (font_size / 2) + margin
    text(e, 1, s, textX, textY, font_size, font, attrib=textAttrib)
    return e


def clamp(x, low, high):
    if x <= low:
        return low
    if x >= high:
        return high
    return x


def makeColor(r, g, b):
    return "#%x%x%x" % (clamp(r, 0, 255), clamp(g, 0, 255), clamp(b, 0, 255))


class StyleSet:
    pass


class ASVGStyle(StyleSet):
    default = "#000000"
    fg = "#000000"
    bg = "#ffffff"
    emph = "#ff0000"
    omit = "#aaaaaa"


class IEEESize:
    width = 8.5 * 72  # pt
    height = 11.0 * 72  # pt

    tb_margin = 1.0 * 72  # pt
    lr_margin = 0.75 * 72  # pt
    column_space = 0.25 * 72  # pt

    text_size = 10  # pt

    one_col_width = (width - lr_margin * 2 - column_space) / 2
    two_col_width = width - lr_margin * 2

    max_height = height - 2 * tb_margin
