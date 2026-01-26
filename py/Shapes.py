from Object import *
from AABB import AABB
from ObjectDAG import *
from random import randint


def random_color():
    return (randint(0, 255), randint(0, 255), randint(0, 255))


class Sphere(Prim):
    def __init__(self, r, T=None, color=None):

        bbox = AABB(
            (-r, -r, -r),
            (r, r, r),
        )

        if color is None:
            color = random_color()

        super().__init__(SphereDAG(r), color, T, bbox)


class Tore(Prim):
    def __init__(self, r, R, T=None, color=None):

        if color is None:
            color = random_color()

        bbox = AABB((-r - R, -r, -r - R), (r + R, r, r + R))

        super().__init__(ToreDAG(r, R), color, T, bbox)


class Roman(Prim):
    def __init__(self, T=None, color=None):
        if color is None:
            color = random_color()

        bbox = AABB((-1, -1, -1), (1, 1, 1))

        super().__init__(RomanDAG(), color, T, bbox)

    def normale(self, x, y, z):
        a = 2.0 * x * y * y + 2.0 * x * z * z - 2.0 * y * z
        b = 2.0 * y * x * x + 2.0 * y * z * z - 2.0 * x * z
        c = 2.0 * z * x * x + 2.0 * z * y * y - 2.0 * x * y

        (a, b, c) = (a, b, c)

        return normalize3((a, b, c))


class Steiner2(Prim):
    def __init__(self, T=None, color=None):
        if color is None:
            color = random_color()

        super().__init__(Steiner2DAG(), color, T, None)


class Steiner4(Prim):
    def __init__(self, T=None, color=None):
        if color is None:
            color = random_color()

        super().__init__(Steiner4DAG(), color, T, None)


class HyperboloidTwoSheets(Prim):
    def __init__(self, T=None, color=None):
        if color is None:
            color = random_color()

        super().__init__(HyperboloidTwoSheetsDAG(), color, T, None)


class HyperboloidOneSheet(Prim):
    def __init__(self, T=None, color=None):
        if color is None:
            color = random_color()

        super().__init__(HyperboloidOneSheetDAG(), color, T, None)
