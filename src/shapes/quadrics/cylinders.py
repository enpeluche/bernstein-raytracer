from ...geometry import Primitive
from ...DAG import x, y, z
from ...geometry import AABB

# Define canonical (unit-space) parameters for infinite cylinders
# Note: Z-axis is infinite as these are uncapped surfaces.
UNIT_CYLINDER = x ** 2 + y ** 2 - 1.0
UNIT_HYPERBOLIC_CYL = x ** 2 - y ** 2 - 1.0
UNIT_PARABOLIC_CYL = x ** 2 + 2.0 * y

CYL_AABB = AABB((-1.0, -1.0, -float("inf")), (1.0, 1.0, float("inf")))


def cylinder(color=None, **kwargs) -> Primitive:

    return Primitive(
        implicit_function=UNIT_CYLINDER,
        color=color,
        aabb=CYL_AABB,
        label="cylinder",
        **kwargs
    )


def elliptic_cylinder(a: float, b: float, color=None, **kwargs) -> Primitive:

    prim = Primitive(
        implicit_function=UNIT_CYLINDER,
        color=color,
        aabb=CYL_AABB,
        label="elliptic_cylinder",
        **kwargs
    )
    prim.scale(a, b, 1.0)

    return prim


def circular_cylinder(radius: float, color=None, **kwargs) -> Primitive:
    prim = Primitive(
        implicit_function=UNIT_CYLINDER,
        color=color,
        aabb=CYL_AABB,
        label="circular_cylinder",
        **kwargs
    )
    prim.scale(radius, radius, 1.0)

    return prim


def hyperbolic_cylinder(a: float, b: float, color=None, **kwargs) -> Primitive:

    prim = Primitive(
        implicit_function=UNIT_HYPERBOLIC_CYL,
        color=color,
        label="hyperbolic_cylinder",
        **kwargs
    )
    prim.scale(a, b, 1.0)

    return prim


def parabolic_cylinder(a: float, color=None, **kwargs) -> Primitive:

    prim = Primitive(
        implicit_function=UNIT_PARABOLIC_CYL,
        color=color,
        label="parabolic_cylinder",
        **kwargs
    )
    prim.scale(1.0, a, 1.0)

    return prim
