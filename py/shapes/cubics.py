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


def taubin_heart(color=None, **kwargs) -> Primitive:
    """
    Gabriel Taubin's Heart Surface.
    A degree 6 algebraic surface with high curvature and deep concavities.
    """
    # On décompose pour la lisibilité (le DAG gérera la simplification)
    # (x^2 + 2.25y^2 + z^2 - 1)^3 - z^3 * (x^2 + 0.1125y^2)

    term1 = (x ** 2 + 2.25 * y ** 2 + z ** 2 - 1) ** 3
    term2 = z ** 3 * (x ** 2 + 0.1125 * y ** 2)

    expr = term1 - term2

    return Primitive(
        implicit_function=expr, color=color, label="Taubin Heart", **kwargs
    )
