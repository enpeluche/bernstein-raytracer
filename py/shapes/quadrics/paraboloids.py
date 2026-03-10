from geometry import Primitive
from DAG import x, y, z

# Define the canonical (unit-space) parameters
# Elliptic: A bowl-shaped surface (x² + y² - z = 0)
# Hyperbolic: A saddle-shaped surface (x² - y² - z = 0)
F_ELLIPTIC = x ** 2 + y ** 2 - z
F_HYPERBOLIC = x ** 2 - y ** 2 - z


def paraboloid(color=None, **kwargs) -> Primitive:

    return Primitive(
        implicit_function=F_ELLIPTIC, color=color, label="paraboloid", **kwargs
    )


def elliptic_paraboloid(a: float, b: float, color=None, **kwargs) -> Primitive:

    prim = Primitive(
        implicit_function=F_ELLIPTIC, color=color, label="elliptic_paraboloid", **kwargs
    )

    prim.scale(a, b, 1.0)

    return prim


def circular_paraboloid(a: float, color=None, **kwargs) -> Primitive:

    prim = Primitive(
        implicit_function=F_ELLIPTIC, color=color, label="circular_paraboloid", **kwargs
    )

    prim.scale(a, a, 1.0)

    return prim


def hyperbolic_paraboloid(a: float, b: float, color=None, **kwargs) -> Primitive:

    prim = Primitive(
        implicit_function=F_HYPERBOLIC,
        color=color,
        label="hyperbolic_paraboloid",
        **kwargs
    )

    prim.scale(a, b, 1.0)

    return prim
