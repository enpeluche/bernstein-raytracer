from geometry import Primitive
from DAG import x, y, z
from geometry import AABB


def cylinder(color, **kwargs):
    aabb = AABB(
        (-1.0, -1.0, -float("inf")),
        (1.0, 1.0, float("inf")),
    )

    return Primitive(
        implicit_function=x ** 2 + y ** 2 - 1.0,
        color=color,
        aabb=aabb,
        label="cylinder",
        **kwargs
    )


def elliptic_cylinder(a, b, color, **kwargs):
    aabb = AABB(
        (-1.0, -1.0, -float("inf")),
        (1.0, 1.0, float("inf")),
    )

    prim = Primitive(
        implicit_function=x ** 2 + y ** 2 - 1.0,
        color=color,
        aabb=aabb,
        label="cylinder",
        **kwargs
    )
    prim.scale(a, b, 1.0)

    return prim


def circular_cylinder(radius, color, **kwargs):
    aabb = AABB(
        (-1.0, -1.0, -float("inf")),
        (1.0, 1.0, float("inf")),
    )

    prim = Primitive(
        implicit_function=x ** 2 + y ** 2 - 1.0,
        color=color,
        aabb=aabb,
        label="cylinder",
        **kwargs
    )
    prim.scale(radius, radius, 1.0)

    return prim


def hyperbolic_cylinder(a, b, color, **kwargs):

    prim = Primitive(
        implicit_function=x ** 2 - y ** 2 - 1.0,
        color=color,
        label="hyperboloid_of_one_sheet",
        **kwargs
    )
    prim.scale(a, b, 1.0)

    return prim


# -------------------------------------------------------------------------------------------------


def parabolic_cylinder(a, color, **kwargs):

    prim = Primitive(
        implicit_function=x ** 2 + 2.0 * y,
        color=color,
        label="parabolic_cylinder",
        **kwargs
    )
    prim.scale(1.0, a, 1.0)

    return prim
