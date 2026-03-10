# from demos import *

from camera import *
from shapes import *
from Scene import Scene
from Renderer import Renderer
from constants import WHITE, DEG

from demos import (
    demo_full_suite,
    camera_0,
    camera_1,
    camera_2,
    camera_3,
    camera_4,
    camera_5,
)


# 1. Prepare your camera rig (the list we defined earlier)
# Make sure all cameras (camera_0 to camera_5) are in this list
my_cameras = [camera_0, camera_1, camera_2, camera_3, camera_4, camera_5]

# 2. Pick your stars (The Primitives Gallery)
# You can mix and match from all your families!
ellipsoids = [
    sphere(radius=0.9, color=(240, 47, 79)),
    ellipsoid(0.6, 0.9, 0.5, color=(47, 240, 150)),
    oblate(0.8, 0.4, color=(47, 150, 240)),
]

cones = [circular_cone(1.0, 0.5), elliptic_cone(0.4, 0.6, 0.3)]

cylinders = [
    cylinder().scale(0.9, 0.9, 0.9),
    elliptic_cylinder(0.5, 0.6),
    circular_cylinder(0.8),
    hyperbolic_cylinder(0.5, 0.33),
    parabolic_cylinder(0.5),
]

hyperboloids = [
    hyperboloid_of_one_sheet(0.8, 0.5, 0.33),
    hyperboloid_of_revolution_of_one_sheet(0.8, 0.5),
    hyperboloid_of_two_sheets(0.8, 0.5, 0.33),
    hyperboloid_of_revolution_of_two_sheets(0.8, 0.5),
]

paraboloids = [
    paraboloid(),
    elliptic_paraboloid(0.8, 0.7),
    circular_paraboloid(0.8),
    hyperbolic_paraboloid(0.7, 0.8),
]

cubics = [cayley().scale(0.7, 0.7, 0.7), whitney_umbrella(), dingdong()]

quartics = [
    roman().scale(0.9, 0.9, 0.9),
    steiner2(),
    steiner4(),
    torus(0.7, 0.3),
]


# taubin_heart = [
#    taubin_heart(color=(240, 47, 79)).scale(0.7, 0.7, 0.7).rotate_y(180 * DEG)
# ]
# demo_full_suite(taubin_heart, my_cameras, "taubin_heart")

# 3. Launch the automated rendering suite

# demo_full_suite(ellipsoids, my_cameras, "quadrics/ellipsoids")
# demo_full_suite(cones, my_cameras, "quadrics/cones")
# demo_full_suite(cylinders, my_cameras, "quadrics/cylinders")
# demo_full_suite(hyperboloids, my_cameras, "quadrics/hyperboloids")
# demo_full_suite(paraboloids, my_cameras, "quadrics/paraboloids")
# demo_full_suite(cubics, my_cameras, "cubics")
# demo_full_suite(quartics, my_cameras, "quartics")

# une render distance

# différent pdv ? pour un format png

# Animations
R = roman(color=(240, 47, 79)).scale(0.9, 0.9, 0.9)
T = taubin_heart(color=(240, 47, 79)).scale(0.7, 0.7, 0.7).rotate_y(180 * DEG)
C = cube()
world = C

for camera in [camera_0]:
    scene = Scene(camera, world)
    renderer = Renderer(scene, name="test", folder=f"cube_rota_z/{camera.name}")
    # C.show_grid = "orthographic" not in camera.name
    for _ in range(90):
        renderer.render()
        C.rotate_z(DEG * 4)
    renderer.save(format="gif")

# Surface de Roman, degré 4

# Instance Roman 0 :
# 500x500 11.46s -> 750x750 08.33s -> 07.32s -> 07.46s -> 1000x1000 09.32s -> 07.84s -> 06.82s -> 06.17s -> 05.70s

# Instance Roman 1 :
# 500x500 10.47s -> 750x750 07.70s -> 07.20s -> 06.65s -> 1000x1000 08.86s -> 08.01s -> 07.44s -> 06.24s -> 06.00s

# Instance Roman 2 :
# 500x500 11.24s -> 750x750 08.07s -> 07.11s -> 05.75s -> 1000x1000 07.77s -> 07.32s -> 06.69s -> 05.45s -> 05.56s

# Instance Roman 3 :
# 500x500 10.33s -> 750x750 06.43s -> 06.06s -> 04.71s -> 1000x1000 06.77s -> 06.67s -> 05.75s -> 04.55s -> 04.65s

# Instance Roman 4 :
# 500x500 10.79s -> 750x750 09.50s -> 07.65s -> 06.72s -> 1000x1000 09.88s -> 09.38s -> 09.54s -> 08.61s -> 08.11s

# Instance Roman 5 :
# 500x500 04.06s -> 750x750 02.70s -> 01.59s -> 01.51s -> 1000x1000 02.00s -> 02.05s -> 02.32s -> 01.96s -> 2.17s
