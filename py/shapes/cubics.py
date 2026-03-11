from geometry import Primitive
from DAG import x, y, z


def whitney_umbrella(color=None, **kwargs) -> Primitive:

    return Primitive(
        implicit_function=x ** 2 - y ** 2 * z,
        color=color,
        label="whitney_umbrella",
        **kwargs
    )


def cayley(color=None, **kwargs) -> Primitive:

    expr = x ** 2 + y ** 2 + z ** 2 + x ** 2 * z - y ** 2 * z - 1.0

    return Primitive(implicit_function=expr, color=color, label="cayley", **kwargs)


def dingdong(color=None, **kwargs) -> Primitive:

    expr = x ** 2 + y ** 2 - (1 - z) * z ** 2

    return Primitive(implicit_function=expr, color=color, label="dingdong", **kwargs)
