from ObjectDAG import *
from Shapes import *
from util import *
from Polynome import *
from Cameras import *
from Object import *
import time
from Transformation import *
from Matrix import *
from Renderer import *
from Transformation import *

PI = 3.1415926565
MESURE = PI / 180.0

# Prim(roman(), (122, 255, 33), AABB((-2, -2, -2), (2, 2, 2)))


# deuxboules = Union(
#    Prim(boule(-0.5, 0, 0, 1), (150, 150, 150)),
#    Prim(boule(0.5, 0, 0, 1), (240, 150, 150)),
# )
camera = CameraPerspective(
    cam_o=(0.0, -4.0, 0.0),
    cam_dx=(1.0, 0.0, 0.0),
    cam_dy=(0.0, 1.0, 0.0),  # la direction des rayons aussi
    cam_dz=(0.0, 0.0, 1.0),
    size_world=1,
    size_win=500,
    light_dir=(-1, -1, 1),
    name="",
    focale=2,
)


def scene():
    H1 = HyperboloidTwoSheets()
    H2 = HyperboloidOneSheet(color=(200, 130, 33))
    return H2


raycasting(camera, scene())
