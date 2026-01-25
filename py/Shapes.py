from Object import *
from AABB import AABB
from ObjectDAG import *


class Sphere(Prim):
    def __init__(self, r, T=None, color=None):

        bbox = AABB(
            (-r, -r, -r),
            (r, r, r),
        )

        super().__init__(SphereDAG(r), color, T, bbox)


class Tore(Prim):
    def __init__(self, r, R, T=None, color=None):

        bbox = AABB((-r - R, -r, -r - R), (r + R, r, r + R))

        super().__init__(ToreDAG(r, R), (33, 144, 222), T, bbox)
