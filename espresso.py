from ocp_vscode import show, show_object, reset_show, set_port, set_defaults, get_defaults
set_port(3939)
from build123d import *

inner_hole_dia = 48.0
inner_depth = 1.5
filter_dia = 58.0
filter_border_r = 3.0
wt = 2.0 # wall thickness
outer_dia = 74.2
x3 = outer_dia / 2


x1 = inner_hole_dia / 2
y1 = -inner_depth
x2 = filter_dia / 2
y2 = 0.0

with BuildPart() as part:
    with BuildSketch(Plane.XZ) as sketch:
        with BuildLine() as line:
            l0 = Line((x1, 3), (x1, y1))
            l1 = Line(l0@1, (x2, y1))
            l2 = Line(l1 @ 1, (x2, y2))
            l3 = ThreePointArc((l2 @ 1, l2 @ 1 + (filter_border_r, filter_border_r)), l2 @ 1 + (filter_border_r * 2, 0))
            l4 = Line(l3 @ 1, l3 @ 1 + (1.5, 0))
            l5 = Line(l4 @ 1, (x3, 2.0))
            l5 = Line(l5 @ 1, (x3, 3.0))
            l6 = ThreePointArc(l5 @ 1, l5 @ 1 + (-3, 8.5), l5 @ 1 + (0, 17))
            l7 = Line(l6 @ 1, (x3, 70))
            l8 = Line(l7 @ 1, l7 @ 1 + (-wt, 0))
            l9 = Line(l8 @ 1, (x3 - wt, 30))
            l10 = JernArc(l9@1, l9%1, radius=30,arc_size=-30)
            l11 = Line(l10@1, l0@0)
        make_face()
    revolve(axis=Axis.Z)

IntersectingLine

show(sketch)
#show(part)