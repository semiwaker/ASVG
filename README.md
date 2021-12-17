# Agile SVG Maker

Need to draw hundreds of frames for a GIF? Need to change the style of all pictures in a PPT? Need to draw similar images with different parameters? Try **ASVG**!

*Under construction, not so agile yet...*

*Basically aimed at academic illustrations.*

## Simple Example

```python
from ASVG import *

# A 500x300 canvas
a = Axis((500, 300)) 

# Draw a rectangle on a, at level 1, from (0,0) to (200,100)
# With (5,5) round corner, fill with red color.
rect(a, 1, 0, 0, 200, 100, 5, 5, fill='red')

# Draw a circle on a, at level 3
# Centered (50,50) with 50 radius, fill with blue color.
circle(a, 3, 50, 50, 50, fill='blue')

# Draw this picture to example.svg
draw(a, "example.svg")
```

## Parameterized Sub-image

```python
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

a = Axis((300,200))
a.addElement(labeledRect(...))
```

## Nested Canvas

### Canvas and Axis

Create a canvas axis with `Axis(size, viewport)`
`size=(width, height)` is the physical size of the canvas in pixels.
`viewport=(x, y)` is the logical size of the axis, by default its the same of the physical size.

```python
# A 1600x900 canvas, axis range [0,1600)x[0,900)
a = Axis((1600, 900))

# A 1600x900 canva, with normalized axis range[0,1),[0,1)
b = Axis((1600, 900), (1.0, 1.0))
```

### ComposedElement

A composed element is a sub-image.

`ComposedElement(size, level, attrib)`
`size=(width, height)`: the size of the axis of this element.
`level`: the higher the level is, the fronter the composed element is.
`attrib`: the common attributes of this element

Add a composed element into the big canvas:`axis.addElement(element, shift)`
`shift=(x,y)` is the displacement of the element in the outer axis.

A composed element can have other composed elements as sub-pictures:
`element.addElement(subElement, shift)`

## Basic Elements

The basic element comes from SVG.
Basicly, every element needs a `axis` and a `level` argument.
`axis` can be a `Axis` or `ComposedElement`.
The bigger the `level` is, the fronter the element is.
`level` is only comparable when two elements are under the same axis.

```python
# Rectangle
rect(
    axis: Union[core.Axis, core.ComposedElement],
    level: int,
    x: float, # top left
    y: float,
    width: float,
    height: float,
    rx: float = 0.0, # round corner radius
    ry: float = 0.0,
    attrib: core.Attrib = core.Attrib(),
    **kwargs
)
# Circle
circle(
    axis: Union[core.Axis, core.ComposedElement],
    level: int,
    cx: float, # center
    cy: float,
    r: float, # radius
    attrib: core.Attrib = core.Attrib(),
    **kwargs
)
# Ellipse
ellipse(
    axis: Union[core.Axis, core.ComposedElement],
    level: int,
    cx: float, # center
    cy: float,
    rx: float, # radius
    ry: float,
    attrib: core.Attrib = core.Attrib(),
    **kwargs
)
# Straight line
line(
    axis: Union[core.Axis, core.ComposedElement],
    level: int,
    x1: float, # Start
    y1: float,
    x2: float, # End
    y2: float,
    attrib: core.Attrib = core.Attrib(),
    **kwargs
)
# Polyline
polyline(
    axis: Union[core.Axis, core.ComposedElement],
    level: int,
    points: List[Tuple[float, float]],
    attrib: core.Attrib = core.Attrib(),
    **kwargs
)
# Polygon
polygon(
    axis: Union[core.Axis, core.ComposedElement],
    level: int,
    points: List[Tuple[float, float]],
    attrib: core.Attrib = core.Attrib(),
    **kwargs
)
# Path
path(
    axis: Union[core.Axis, core.ComposedElement],
    level: int,
    d: PathD,
    attrib: core.Attrib = core.Attrib(),
    **kwargs
)
```

`PathD` is a sequence of path descriptions, the actions is like SVG's path element. View [Path tutorial](https://developer.mozilla.org/en-US/docs/Web/SVG/Tutorial/Paths)
We use `?To()` for captial letters and `?For()` for lower-case letters. `close()` and `open()` is for closing or opening the path.
Example:

```python
d = PathD()
d.moveTo(100,100)
d.hlineFor(90)
d.close()
# Equivilent: d = PathD(["M 80 80", "h 90",  "Z"])

path(a, 0, d)
```

## Text

```python
text(
    axis: Union[core.Axis, core.ComposedElement],
    level: int,
    s: Union[str, TextRepresent],
    x: float,
    y: float,
    fontSize: int,
    font: str = "Arial",
    anchor: str = "middle",
    attrib: core.Attrib = core.Attrib(),
    **kwargs
)
```

`anchor` is where `(x,y)` is in the text. Can be either `start`, `middle` or `end`.

`TextRepresent` means formatted text.
Normal string with `\n` in it will be converted into multilines.
You can use `TextSpan` to add some attributes to a span of text.

Examples:

```python
text(
    a, 10,
    "Hello\n???" + \
    TextSpan("!!!\n", fill='#00ffff', font_size=25) +\
    "???\nabcdef",
    30, 30, 20, anchor="start")
```

## Arrow

```python
# Straight arrow
arrow(
    axis: Union[core.Axis, core.ComposedElement],
    level: int,
    x: float, # Position of the tip
    y: float,
    fromX: float, # Position of the other end
    fromY: float,
    tipSize: float = 10.0,
    tipAngle: float = 60.0,
    tipFilled: bool = True,
    **kwargs
)
# Polyline arrow
polyArrow(
    axis: Union[core.Axis, core.ComposedElement],
    level: int,
    points: List[Tuple[float, float]],
    tipSize: float = 10.0,
    tipAngle: float = 60.0,
    tipFilled: bool = True,
    **kwargs
)
```

## Attributes

Attributes is for customizing the style of the elements.

```python
myStyle = Attrib(
    fill = "#1bcd20",
    stroke = "black",
    stroke_width = "1pt"
)

alertStype = myStyle.copy()
alertStype.fill = "#ff0000"

rect(..., attrib=myStyle)
circle(..., attrib=alertStyle)
```

The name of the attribute are the same as in SVG elements, except use underline `_` instead of dash `-`

Attributs of `ComposedElement` applies on `<group>` element.

For convinent, you can directly write some attributes in `**kwargs`.

```python
rect(..., fill="red")

# Equivilient
rect(..., attrib=Attrib(fill="red))
```

