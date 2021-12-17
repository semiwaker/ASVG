from typing import List, Tuple, Optional, Union

from . import core


def makeBasicElement(name: str, indent: int, attrib: core.Attrib) -> core.SVGLines:
    return [" " * indent + f"<{name} {attrib} />"]


class BasicElement(core.Element):
    def __init__(self, **kwargs):
        if isinstance(kwargs["axis"], core.ComposedElement):
            kwargs["axis"] = kwargs["axis"].axis
        super(BasicElement, self).__init__(
            kwargs["axis"], kwargs["level"], kwargs["attrib"])
        self.SVGType = kwargs["SVGType"]
        for k, v in kwargs.items():
            if k not in {"SVGType", "axis", "level", "attrib"}:
                self.attrib.__dict__[k] = v

    def makeSVG(self, indent: int = 0) -> core.SVGLines:
        return makeBasicElement(self.SVGType, indent, self.attrib)


def rect(
    axis: Union[core.Axis, core.ComposedElement],
    level: int,
    x: float,
    y: float,
    width: float,
    height: float,
    rx: float = 0.0,
    ry: float = 0.0,
    attrib: core.Attrib = core.Attrib(),
    **kwargs
):
    return BasicElement(
        SVGType="rect",
        axis=axis,
        level=level,
        x=x,
        y=y,
        width=width,
        height=height,
        rx=rx,
        ry=ry,
        attrib=attrib,
        **kwargs
    )


def circle(
    axis: Union[core.Axis, core.ComposedElement],
    level: int,
    cx: float,
    cy: float,
    r: float,
    attrib: core.Attrib = core.Attrib(),
    **kwargs
):
    return BasicElement(
        SVGType="circle",
        axis=axis,
        level=level,
        cx=cx,
        cy=cy,
        r=r,
        attrib=attrib,
        **kwargs
    )


def ellipse(
    axis: Union[core.Axis, core.ComposedElement],
    level: int,
    cx: float,
    cy: float,
    rx: float,
    ry: float,
    attrib: core.Attrib = core.Attrib(),
    **kwargs
):
    return BasicElement(
        SVGType="ellipse",
        axis=axis,
        level=level,
        cx=cx,
        cy=cy,
        rx=rx,
        ry=ry,
        attrib=attrib,
        **kwargs
    )


def line(
    axis: Union[core.Axis, core.ComposedElement],
    level: int,
    x1: float,
    y1: float,
    x2: float,
    y2: float,
    attrib: core.Attrib = core.Attrib(),
    **kwargs
):
    return BasicElement(
        SVGType="line",
        axis=axis,
        level=level,
        x1=x1,
        y1=y1,
        x2=x2,
        y2=y2,
        attrib=attrib,
        **kwargs
    )


def polyline(
    axis: Union[core.Axis, core.ComposedElement],
    level: int,
    points: List[Tuple[float, float]],
    attrib: core.Attrib = core.Attrib(),
    **kwargs
):
    if not hasattr(attrib, "fill") and "fill" not in kwargs:
        kwargs["fill"] = "transparent"
    return BasicElement(
        SVGType="polyline",
        axis=axis,
        level=level,
        points=", ".join([f"{x} {y}"for x, y in points]),
        attrib=attrib,
        **kwargs
    )


def polygon(
    axis: Union[core.Axis, core.ComposedElement],
    level: int,
    points: List[Tuple[float, float]],
    attrib: core.Attrib = core.Attrib(),
    **kwargs
):
    return BasicElement(
        SVGType="polygon",
        axis=axis,
        level=level,
        points=", ".join([f"{x} {y}"for x, y in points]),
        attrib=attrib,
        **kwargs
    )


class PathD:
    def __init__(self, isClosed: bool = False, commands: List[str] = []):
        self.isClosed = isClosed
        self.commands = commands

    def moveTo(self, x: float, y: float):
        self.commands.append(f"M {x} {y}")

    def moveFor(self, dx: float, dy: float):
        self.commands.append(f"m {dx} {dy}")

    def lineTo(self, x: float, y: float):
        self.commands.append(f"L {x} {y}")

    def lineFor(self, dx: float, dy: float):
        self.commands.append(f"l {dx} {dy}")

    def hlineTo(self, x: float):
        self.commands.append(f"H {x}")

    def hlineFor(self, dx: float):
        self.commands.append(f"h {dx}")

    def vlineTo(self, y: float):
        self.commands.append(f"V {y}")

    def vlineFor(self, dy: float):
        self.commands.append(f"v {dy}")

    def curveTo(self, x1: float, y1: float, x2: float, y2: float, x: float, y: float):
        self.commands.append(f"C {x1} {y1}, {x2} {y2}, {x} {y}")

    def curveFor(self, dx1: float, dy1: float, dx2: float, dy2: float, dx: float, dy: float):
        self.commands.append(f"c {dx1} {dy1}, {dx2} {dy2}, {dx} {dy}")

    def STo(self, x2: float, y2: float, x: float, y: float):
        self.commands.append(f"S {x2} {y2}, {x} {y}")

    def SFor(self, dx2: float, dy2: float, dx: float, dy: float):
        self.commands.append(f"s {dx2} {dy2}, {dx} {dy}")

    def QTo(self, x2: float, y2: float, x: float, y: float):
        self.commands.append(f"Q {x2} {y2}, {x} {y}")

    def QFor(self, dx2: float, dy2: float, dx: float, dy: float):
        self.commands.append(f"q {dx2} {dy2}, {dx} {dy}")

    def TTo(self, x: float, y: float):
        self.commands.append(f"T {x} {y}")

    def TFor(self, dx: float, dy: float):
        self.commands.append(f"t {dx} {dy}")

    def arcTo(
        self,
        rx: float,
        ry: float,
        xAxisRotation: float,
        largeArc: Union[int, bool],
        sweep: Union[int, bool],
        x: float,
        y: float
    ):
        self.commands.append(
            f"A {rx} {ry} {xAxisRotation} {int(largeArc)} {int(sweep)} {x} {y}")

    def arcFor(
        self,
        rx: float,
        ry: float,
        xAxisRotation: float,
        largeArc: Union[int, bool],
        sweep: Union[int, bool],
        dx: float,
        dy: float
    ):
        self.commands.append(
            f"a {rx} {ry} {xAxisRotation} {int(largeArc)} {int(sweep)} {dx} {dy}")

    def close(self):
        self.isClosed = True

    def open(self):
        self.isClosed = False

    def __str__(self) -> str:
        s = " ".join(self.commands).strip()
        if s[-1] != 'Z' and s[-1] != 'z' and self.isClosed:
            s += " Z"
        return s


def path(
    axis: Union[core.Axis, core.ComposedElement],
    level: int,
    d: PathD,
    attrib: core.Attrib = core.Attrib(),
    **kwargs
):
    return BasicElement(
        SVGType="polygon",
        axis=axis,
        level=level,
        d=d,
        attrib=attrib,
        **kwargs
    )
