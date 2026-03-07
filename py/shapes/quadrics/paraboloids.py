from geometry import Primitive
from DAG import x, y, z


def paraboloid(color, **kwargs):

    return Primitive(
        implicit_function=x ** 2 + y ** 2 - z, color=color, label="paraboloid", **kwargs
    )


def elliptic_paraboloid(a, b, color, **kwargs):

    prim = Primitive(
        implicit_function=x ** 2 + y ** 2 - z,
        color=color,
        label="elliptic_paraboloid",
        **kwargs
    )

    prim.scale(a, b, 1.0)

    return prim


def circular_paraboloid(a, color, **kwargs):

    prim = Primitive(
        implicit_function=x ** 2 + y ** 2 - z,
        color=color,
        label="circular_paraboloid",
        **kwargs
    )

    prim.scale(a, a, 1.0)

    return prim


def hyperbolic_paraboloid(a, b, color, **kwargs):

    prim = Primitive(
        implicit_function=x ** 2 + y ** 2 - z,
        color=color,
        label="circular_paraboloid",
        **kwargs
    )

    prim.scale(a, b, 1.0)

    return prim
