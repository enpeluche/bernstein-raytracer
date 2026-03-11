from geometry import Primitive
from DAG import x, y, z
from geometry import AABB


def taubin_heart(color=None, **kwargs) -> Primitive:
    """
    Gabriel Taubin's Heart Surface.
    A degree 6 algebraic surface with high curvature and deep concavities.
    """

    term1 = (x ** 2 + 2.25 * y ** 2 + z ** 2 - 1) ** 3
    term2 = z ** 3 * (x ** 2 + 0.1125 * y ** 2)

    expr = term1 - term2

    return Primitive(
        implicit_function=expr, color=color, label="Taubin Heart", **kwargs
    )
