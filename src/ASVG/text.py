from html import escape
from typing import Union, List, overload

from . import core


class TextRepresent:
    def __init__(self, fontSize: int = -1):
        self.fontSize = fontSize

    def __add__(self, s: str):
        return TextGroup([self, s])

    def __radd__(self, s: str):
        return TextGroup([s, self])

    def _overloadFontSize(self, size: int):
        if self.fontSize == -1:
            self.fontSize = size

    def _splitRow(self):
        return []

    def makeSVG(self, indent: int = 0) -> core.SVGLines:
        return []


class TextGroup(TextRepresent):
    def __init__(self, texts):
        super(TextGroup, self).__init__(
            max(map(lambda t: t.fontSize if isinstance(t, TextRepresent) else -1, texts)))
        self.texts = []
        for t in texts:
            if isinstance(t, TextGroup):
                self.texts.extend(t.texts)
            else:
                if t != "" and not (isinstance(t, TextSpan) and t.s == ""):
                    self.texts.append(t)

    @overload
    def __add__(self, s: str):
        return TextGroup(self.texts + [s])

    @overload
    def __add__(self, s: TextRepresent):
        if isinstance(s, TextGroup):
            return TextGroup(self.texts + s.texts)
        else:
            return TextGroup(self.tests + [s])

    def __add__(self, s):
        return TextGroup(self.texts + [s])

    def _overloadFontSize(self, size: int):
        for t in self.texts:
            if not isinstance(t, str):
                t._overloadFontSize(size)
        self.fontSize = max(self.fontSize, size)

    def _splitRow(self):
        result = []
        curRow = []

        def makeGroup(row):
            if len(row) == 1 and isinstance(row, TextSpan):
                return row[0]
            else:
                return TextGroup(row)

        def appendRow(r):
            nonlocal curRow
            curRow.append(r)
            result.append(makeGroup(curRow))
            curRow = []

        def appendRows(rows):
            if len(rows) == 1:
                curRow.append(rows[0])
            else:
                for r in rows[:-1]:
                    appendRow(r)
                curRow.append(rows[-1])

        for t in self.texts:
            if isinstance(t, str):
                appendRows([TextGroup([i]) for i in t.split('\n')])
            else:
                appendRows(t._splitRow())

        if len(curRow) > 0:
            result.append(makeGroup(curRow))

        return result

    def makeSVG(self, indent: int = 0) -> core.SVGLines:
        result = []
        for t in self.texts:
            if isinstance(t, TextRepresent):
                result.extend(t.makeSVG(indent))
            else:
                result.append(escape(t))
        return result


class TextSpan(TextRepresent):
    def __init__(
        self,
        s: Union[str, TextRepresent],
        attrib: core.Attrib = core.Attrib(),
        **kwargs
    ):
        self.s = s
        self.attrib = attrib + kwargs

        if isinstance(self.s, TextRepresent):
            fontSize = s.fontSize
        else:
            fontSize = -1

        super(TextSpan, self).__init__(
            max(fontSize,
                getattr(self.attrib, "fontSize", -1),
                getattr(self.attrib, "font_size", -1))
        )

    def _overloadFontSize(self, size: int):
        if isinstance(self.s, TextRepresent):
            self.s._overloadFontSize(size)
            self.fontSize = self.s.fontSize
        elif self.fontSize == -1:
            self.fontSize = size

    def _splitRow(self):
        if isinstance(self.s, str):
            splited = self.s.split('\n')
        else:
            splited = self.s._splitRow()
        return [TextSpan(s, self.attrib) for s in splited]

    def makeSVG(self, indent: int) -> core.SVGLines:
        if isinstance(self.s, str):
            svg = [escape(self.s)]
        else:
            svg = self.s.makeSVG(indent + core.INDENT)
        return [" " * indent + f"<tspan {self.attrib}>"] + svg + [" " * indent + "</tspan>"]


class Text(core.Element):
    def __init__(self, **kwargs):
        if isinstance(kwargs["axis"], core.ComposedElement):
            kwargs["axis"] = kwargs["axis"].axis
        super(Text, self).__init__(
            kwargs["axis"], kwargs["level"], kwargs["attrib"])

        self.s = kwargs["s"]
        if isinstance(self.s, str):
            self.s = TextGroup([self.s])
        self.rows = self.s._splitRow()
        for r in self.rows:
            r._overloadFontSize(kwargs["font_size"])

        for k, v in kwargs.items():
            if k not in {"s", "axis", "level", "attrib"}:
                self.attrib.__dict__[k] = v

    def makeSVG(self, indent: int) -> core.SVGLines:
        result = []
        attrib = self.attrib.copy()
        first = True
        for r in self.rows:
            if not first:
                attrib.y += r.fontSize
            else:
                first = False
            result.append(" " * indent + f"<text {attrib}>")
            result.extend(r.makeSVG(indent + core.INDENT))
            result.append(" " * indent + "</text>")
        return result


def text(axis: Union[core.Axis, core.ComposedElement],
         level: int,
         s: Union[str, TextRepresent],
         x: float,
         y: float,
         fontSize: int,
         font: str = "Arial",
         anchor: str = "middle",
         attrib: core.Attrib = core.Attrib(),
         **kwargs
         ) -> core.SVGLines:
    return Text(
        axis=axis,
        level=level,
        s=s,
        x=x,
        y=y,
        font_size=fontSize,
        font_family=font,
        text_anchor=anchor,
        attrib=attrib,
        **kwargs
    )
