import copy
from typing import Tuple, Optional, List

INDENT = 2


class Attrib:
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            self.__dict__[k] = v

    def __add__(self, other):
        result = self.copy()
        if isinstance(other, dict):
            for k, v in other.items():
                result.__dict__[k] = v
        else:
            for k, v in other.__dict__.items():
                result.__dict__[k] = v
        return result

    def copy(self):
        return copy.copy(self)

    def __str__(self) -> str:
        s = []
        for k, v in self.__dict__.items():
            replacedk = k.replace('_', '-')
            s.append(f'{replacedk}="{v}"')
        return " ".join(s)


SVGLines = List[str]


class SVGMaker:
    def makeSVG(self, indent: int = 0) -> SVGLines:
        return []


class Axis(SVGMaker):
    def __init__(self, size: Tuple[float, float], viewBox: Optional[Tuple[float, float, float, float]] = None):
        self.size = size
        self.w, self.h = size
        self.attrib = Attrib(
            xmlns="http://www.w3.org/2000/svg",
            width=self.w,
            height=self.h)
        if viewBox is not None:
            self.attrib.viewBox = " ".join(map(str, viewBox))

        self.elements = []

    def addElement(self, element, shift: Tuple[float, float] = (0, 0)):
        if element.axis != self:
            element.axis.setShift(shift)
        self.elements.append(element)

    def removeElement(self, element):
        self.elements.remove(element)

    def setShift(self, shift: Tuple[float, float]):
        self.attrib.x, self.attrib.y = shift
        del self.attrib.xmlns

    def makeSVG(self, indent: int = 0) -> SVGLines:
        result = [
            " " * indent + f"<svg {self.attrib}>"]
        self.elements.sort(key=lambda e: e.level, reverse=False)
        for e in self.elements:
            result.extend(e.makeSVG(indent + INDENT))
        result.append(" "*indent + "</svg>")
        return result


class Element(SVGMaker):
    def __init__(self, axis: Axis, level: int, attrib: Attrib = Attrib()):
        self.axis = axis
        self.level = level
        self.attrib = attrib.copy()

        axis.addElement(self)

    def makeSVG(self, indent: int = 0) -> SVGLines:
        return []


class ComposedElement(Element):
    def __init__(self, size: Tuple[float, float], level: int, attrib: Attrib = Attrib()):
        super(ComposedElement, self).__init__(Axis(size), level, attrib)
        self.axis.removeElement(self)

    def addElement(self, element, shift: Tuple[float, float] = (0, 0)):
        self.axis.addElement(element, shift)

    def makeSVG(self, indent: int = 0) -> SVGLines:
        svg = self.axis.makeSVG(indent)
        if len(self.attrib.__dict__):
            svg.insert(1, " " * indent + f"<g {self.attrib}>")
            svg.insert(-1, " " * indent + f"</g>")
        return svg
