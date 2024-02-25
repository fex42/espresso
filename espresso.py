from ocp_vscode import show, show_object, reset_show, set_port, set_defaults, get_defaults
set_port(3939)
from build123d import *

wt = 2.0 # wall thickness
tol = 0.4 # tolerance distance between parts

inner_hole_dia = 48.0
filter_dia1 = 58.0
filter_border_w = 6.0
outer_dia = 74.2

height = 60.0

r1 = outer_dia / 2
r2 = filter_dia1 / 2
r3 = inner_hole_dia / 2
filter_border_r = filter_border_w / 2

with BuildPart() as body:
    with BuildSketch(Plane.XZ) as body_sk:
        with BuildLine():
            c1 = Line((r1 - wt, 0), (r1 - wt, height), mode=Mode.PRIVATE) # construction line
            l1 = Line((r3, 0), (r3, 4.5))
            l2 = IntersectingLine(l1@1, Vector(0.5, 0.71), c1)
            l3 = Line(l2@1, ((l2@1).X, height))
            l4 = Line(l3@1, (r1, height))

            l5 = Line(l1@0, (r2 , (l1@0).Y))
            l6 = PolarLine(l5@1, 1.5, 90.0)
            l7 = ThreePointArc((l6@1, 
                                l6@1 + (filter_border_r, filter_border_r)),
                                l6@1 + (filter_border_r * 2, 0))
            l8 = Line(l7@1, l7@1 + (1.5, 0))
            l9 = Line(l8@ 1, (r1, 2.0))
            l10 = Line(l9@ 1, (r1, 3.0))
            l11 = ThreePointArc(l10@1, 
                               l10@1 + (-3, 9), 
                               l10@1 + (0, 18))
            l12 = Line(l11@1, l4@1)
        make_face()
    revolve(axis=Axis.Z)
    fillet(body.edges().filter_by_position(Axis.Z, 
                                           minimum=10.0, 
                                           maximum=40.0), 
                                           30.0)

show(body)
