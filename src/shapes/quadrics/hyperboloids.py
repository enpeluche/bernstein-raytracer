from ...geometry import Primitive
from ...DAG import x, y, z

# Define the canonical (unit-space) parameters
# One sheet: A continuous surface (like a cooling tower)
# Two sheets: Two separate bowls facing each other
F_ONE_SHEET = x ** 2 + y ** 2 - z ** 2 - 1.0
F_TWO_SHEETS = x ** 2 + y ** 2 - z ** 2 + 1.0


def hyperboloid_of_one_sheet(
    a: float, b: float, c: float, color=None, **kwargs
) -> Primitive:

    prim = Primitive(
        implicit_function=F_ONE_SHEET,
        color=color,
        label="hyperboloid_of_one_sheet",
        **kwargs
    )

    prim.scale(a, b, c)

    return prim


def hyperboloid_of_revolution_of_one_sheet(
    a: float, b: float, color=None, **kwargs
) -> Primitive:

    prim = Primitive(
        implicit_function=F_ONE_SHEET,
        color=color,
        label="hyperboloid_of_revolution_of_one_sheet",
        **kwargs
    )

    prim.scale(a, a, b)

    return prim


def hyperboloid_of_two_sheets(
    a: float, b: float, c: float, color=None, **kwargs
) -> Primitive:

    prim = Primitive(
        implicit_function=F_TWO_SHEETS,
        color=color,
        label="hyperboloid_of_two_sheets",
        **kwargs
    )

    prim.scale(a, b, c)

    return prim


def hyperboloid_of_revolution_of_two_sheets(a, b, color=None, **kwargs) -> Primitive:

    prim = Primitive(
        implicit_function=F_TWO_SHEETS,
        color=color,
        label="hyperboloid_of_revolution_of_two_sheets",
        **kwargs
    )

    prim.scale(a, a, b)

    return prim
