from geometry import Primitive
from DAG import x, y, z


def hyperboloid_of_one_sheet(a, b, c, color, **kwargs):

    expr = x ** 2 + y ** 2 - z ** 2 - 0.1

    prim = Primitive(
        implicit_function=expr, color=color, label="hyperboloid_of_one_sheet", **kwargs
    )

    prim.scale(a, b, c)

    return prim


def hyperboloid_of_revolution_of_one_sheet(a, b, color, **kwargs):

    prim = Primitive(
        implicit_function=x ** 2 + y ** 2 - z ** 2 - 0.1,
        color=color,
        label="hyperboloid_of_revolution_of_one_sheet",
        **kwargs
    )

    prim.scale(a, a, b)

    return prim


# -------------------------------------------------------------------------------------------------
def hyperboloid_of_two_sheets(a, b, c, color, **kwargs):

    prim = Primitive(
        implicit_function=x ** 2 + y ** 2 - z ** 2 + 0.1,
        color=color,
        label="hyperboloid_of_two_sheets",
        **kwargs
    )

    prim.scale(a, b, c)

    return prim


def hyperboloid_of_revolution_of_two_sheets(a, b, color, **kwargs):

    prim = Primitive(
        implicit_function=x ** 2 + y ** 2 - z ** 2 + 0.1,
        color=color,
        label="hyperboloid_of_revolution_of_two_sheets",
        **kwargs
    )

    prim.scale(a, a, b)

    return prim
