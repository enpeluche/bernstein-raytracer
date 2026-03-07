from geometry import Primitive
from DAG import x, y, z
from geometry import AABB


def sphere(radius=1.0, color=None, **kwargs):
    prim = Primitive(
        implicit_function=x ** 2 + y ** 2 + z ** 2 - 1.0,
        color=color,
        aabb=AABB((-1.0, -1.0, -1.0), (1.0, 1.0, 1.0)),
        label="sphere",
        **kwargs
    )

    if radius != 1.0:
        prim.scale(radius, radius, radius)

    return prim


def ellipsoid(a, b, c, color, **kwargs):
    prim = Primitive(
        implicit_function=x ** 2 + y ** 2 + z ** 2 - 1.0,
        color=color,
        aabb=AABB((-1.0, -1.0, -1.0), (1.0, 1.0, 1.0)),
        label="ellipsoid",
        **kwargs
    )

    prim.scale(a, b, c)

    return prim


def oblate(radius, height, color, **kwargs):
    prim = Primitive(
        implicit_function=x ** 2 + y ** 2 + z ** 2 - 1.0,
        color=color,
        aabb=AABB((-1.0, -1.0, -1.0), (1.0, 1.0, 1.0)),
        label="oblate",
        **kwargs
    )

    prim.scale(radius, radius, height)

    return prim
