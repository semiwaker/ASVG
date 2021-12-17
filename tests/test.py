from ASVG import *

a = Axis((500, 300))
rect(a, 1, 0, 0, 200, 100, 5, 5, fill='red')
circle(a, 3, 50, 50, 50, fill='blue')
text(a, 10, "Hello\n???" + TextSpan("!!!\n", fill='#00ffff',
     font_size=25) + "???\nabcdef", 30, 30, 20, anchor="start")

e2 = ComposedElement((100, 100), 2)
ellipse(e2, 1, 20, 30, 20, 30, fill='green')
polygon(e2, 2, [(5, 5), (80, 80), (80, 5)],
        fill='transparent',
        stroke='yellow',
        stroke_width='5',
        stroke_dasharray="5,5")
e2.attrib.transform = "rotate(50 50, 45)"
a.addElement(e2, (50, 50))

e3 = labeledCircle(1, 20, "PE", 20,
                   textShift=(0, -3),
                   circleAttrib=Attrib(
                       fill="white", stroke="black", stroke_width="2"),
                   textAttrib=Attrib(fill="black"))
a.addElement(e3, (100, 80))

draw(a, "test.svg")
