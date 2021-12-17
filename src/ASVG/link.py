from ASVG.core import *
from ASVG.basicElements import *

import math


def arrowTip(
    axis: Union[core.Axis, core.ComposedElement],
    level: int,
    x: float,
    y: float,
    fromX: float,
    fromY: float,
    size: float = 10.0,
    angle: float = 60.0,
    filled: bool = True,
    **kwargs
):
    if filled:
        if "stroke" in kwargs:
            fill = kwargs["stroke"]
        else:
            fill = "#000000"
    else:
        fill = "transparent"
        if "fill" in kwargs:
            kwargs["fill"] = fill

    angle *= math.pi / 360.0
    dx = fromX - x
    dy = fromY - y

    l = math.sqrt(dx * dx + dy * dy)
    dx *= size / l
    dy *= size / l

    dx1 = dx * math.cos(angle) - dy * math.sin(angle)
    dy1 = dx * math.sin(angle) + dy * math.cos(angle)

    dx2 = dx * math.cos(angle) + dy * math.sin(angle)
    dy2 = - dx * math.sin(angle) + dy * math.cos(angle)

    c0 = (x, y)
    c1 = (x + dx1, y + dy1)
    c2 = (x + dx2, y + dy2)

    if filled:
        if "fill" in kwargs:
            polygon(axis, level, [c0, c1, c2], **kwargs)
        else:
            polygon(axis, level, [c0, c1, c2], fill=fill, **kwargs)
    else:
        line(axis, level, x, y, c1[0], c1[1], **kwargs)
        line(axis, level, x, y, c2[0], c2[1], **kwargs)


def arrow(
    axis: Union[core.Axis, core.ComposedElement],
    level: int,
    x: float,
    y: float,
    fromX: float,
    fromY: float,
    tipSize: float = 10.0,
    tipAngle: float = 60.0,
    tipFilled: bool = True,
    **kwargs
):
    arrowTip(axis, level, x, y, fromX, fromY,
             tipSize, tipAngle, tipFilled, **kwargs)
    line(axis, level, x, y, fromX, fromY, **kwargs)


def polyArrow(
    axis: Union[core.Axis, core.ComposedElement],
    level: int,
    points: List[Tuple[float, float]],
    tipSize: float = 10.0,
    tipAngle: float = 60.0,
    tipFilled: bool = True,
    **kwargs
):
    polyline(axis, level, points, **kwargs)
    arrowTip(axis, level, points[-1][0], points[-1][1], points[-2][0], points[-2][1],
             tipSize, tipAngle, tipFilled, **kwargs)
