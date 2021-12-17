from ASVG import *

a = Axis((500, 500))

polyArrow(a, 0, [(10, 10), (10, 30), (50, 30), (50, 100)],
          tipFilled=True,
          stroke=ASVGStyle.omit,
          stroke_width=3)

draw(a, "test.svg")
