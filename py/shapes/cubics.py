from geometry import Primitive
from DAG import x, y, z


def whitney_umbrella(color=None, **kwargs):

    return Primitive(
        implicit_function=x ** 2 - y ** 2 * z,
        color=color,
        label="whitney_umbrella",
        **kwargs
    )


def cayley(color=None, **kwargs):

    expr = x ** 2 + y ** 2 + z ** 2 + x ** 2 * z - y ** 2 * z - 1.0

    return Primitive(implicit_function=expr, color=color, label="cayley", **kwargs)
