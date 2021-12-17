from os import path
from typing import Optional

from . import core


class BasePainter:
    def __call__(self, element: core.Element, file: Optional[str] = None) -> str:
        return ""


class DefaultPainter(BasePainter):
    def __init__(self):
        pass

    def __call__(self, element: core.Element, file: Optional[str] = None) -> str:
        svgs = element.makeSVG()
        s = "\n".join(svgs)
        if file is not None:
            with open(file, "w", encoding="utf-8") as fout:
                fout.write(s)
        return s


def draw(element: core.Element, file: Optional[str] = None, painter: BasePainter = DefaultPainter()) -> str:
    return painter(element, file)
