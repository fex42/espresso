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
    
with BuildPart() as cover:
    with BuildSketch(Plane.XZ) as cover_sk:
        with BuildLine():
            r = r1 - wt - tol
            h = height - wt + tol
            l1 = Line((0,h), (r,h))
            l2 = Line(l1@1, (r, h+wt))
            l3 = Line(l2@1, (r1, h+wt))
            l4 = Line(l3@1, (r1, height+wt))
            l5 = Line(l4@1, (0, height+wt))
            l6 = Line(l5@1, l1@0)
        make_face()
        with Locations((0, height-4.0)):
            Circle(4.2, mode=Mode.SUBTRACT)
    revolve(axis=Axis.Z)

with BuildPart() as inner:
    with BuildSketch(Plane.XZ) as cover_sk:
        with BuildLine():
            h = 7.5
            h2 = height - wt
            cl = Line((0, h), (r1, h), mode=Mode.PRIVATE)
            l1 = Line((0,1.5), (r3-tol, 1.5))
            l2 = Line(l1@1, ((l1@1).X, 4.5 + tol/2))
            l3 = IntersectingLine(l2@1, Vector(0.5, 0.71), cl)
            l3h = PolarLine(l3@1, tol, 90)
            l4 = Line(l3h@1, (2.5 ,h+3))
            l5 = Line(l4@1, ((l4@1).X, h2))
            l6 = Line(l5@1, (0,h2))
            le = Line(l6@1, l1@0)
        make_face()
    revolve(axis=Axis.Z)
    with Locations((0,0,height-4.2)):
        Sphere(4.0)
    fillet(inner.edges().filter_by_position(Axis.Z, 
                                           minimum=10.0, 
                                           maximum=height - 6), 
                                           23.0)

show(body, cover, inner)

version="-v1"
body.part.export_step("body" + version + ".step")
cover.part.export_step("cover" + version + ".step")
inner.part.export_step("inner" + version + ".step")