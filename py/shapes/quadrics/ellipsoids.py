from geometry import Primitive
from DAG import x, y, z
from geometry import AABB

# Define the canonical (unit-space) parameters used as templates for all shapes
UNIT_SPHERE = x ** 2 + y ** 2 + z ** 2 - 1.0
UNIT_AABB = AABB((-1.0, -1.0, -1.0), (1.0, 1.0, 1.0))


def sphere(radius: float = 1.0, color=None, **kwargs) -> Primitive:
    prim = Primitive(
        implicit_function=UNIT_SPHERE,
        color=color,
        aabb=UNIT_AABB,
        label="sphere",
        **kwargs
    )

    if radius != 1.0:
        prim.scale(radius, radius, radius)

    return prim


def ellipsoid(a: float, b: float, c: float, color=None, **kwargs) -> Primitive:
    prim = Primitive(
        implicit_function=UNIT_SPHERE,
        color=color,
        aabb=UNIT_AABB,
        label="ellipsoid",
        **kwargs
    )

    prim.scale(a, b, c)

    return prim


def oblate(radius: float, height: float, color=None, **kwargs) -> Primitive:
    prim = Primitive(
        implicit_function=UNIT_SPHERE,
        color=color,
        aabb=UNIT_AABB,
        label="oblate",
        **kwargs
    )

    prim.scale(radius, radius, height)

    return prim
