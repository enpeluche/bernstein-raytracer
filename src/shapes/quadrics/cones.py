from ...geometry import Primitive
from ...DAG import x, y, z

# Define the canonical (unit-space) parameters for infinite cones
# Equation: x² + y² - z² = 0 (Double cone meeting at origin)
UNIT_CONE = x ** 2 + y ** 2 - z ** 2


def elliptic_cone(a: float, b: float, c: float, color=None, **kwargs) -> Primitive:
    prim = Primitive(
        implicit_function=UNIT_CONE, color=color, label="elliptic_cone", **kwargs
    )

    prim.scale(a, b, c)

    return prim


def circular_cone(radius: float, height: float, color=None, **kwargs) -> Primitive:

    prim = Primitive(
        implicit_function=UNIT_CONE, color=color, label="circular_cone", **kwargs
    )

    prim.scale(radius, radius, height)

    return prim
