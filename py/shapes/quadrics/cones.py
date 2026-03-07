from geometry import Primitive
from DAG import x, y, z


def elliptic_cone(a, b, c, color, **kwargs):
    prim = Primitive(
        implicit_function=x ** 2 + y ** 2 - z ** 2,
        color=color,
        label="hyperboloid_of_one_sheet",
        **kwargs
    )

    prim.scale(a, b, c)

    return prim


def circular_cone(radius, height, color, **kwargs):

    prim = Primitive(
        implicit_function=x ** 2 + y ** 2 - z ** 2,
        color=color,
        label="hyperboloid_of_one_sheet",
        **kwargs
    )

    prim.scale(radius, radius, height)

    return prim
