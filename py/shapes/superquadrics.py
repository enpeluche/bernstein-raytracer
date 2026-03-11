from geometry import Primitive
from DAG import x, y, z
from geometry import AABB


def algebraic_cube(k, color=None, **kwargs) -> Primitive:
    return Primitive(
        implicit_function=x ** k + y ** k + z ** k - 1,
        color=color,
        aabb=AABB((-1.0, -1.0, -1.0), (1.0, 1.0, 1.0)),
        label=f"algebraic_cube_{k}",
        **kwargs,
    )


def monster(k, color=None, **kwargs) -> Primitive:
    return Primitive(
        implicit_function=x ** k + y ** k + z ** k - x ** 2 * y ** 2 * z ** 2 - 1,
        color=color,
        aabb=AABB((-1.0, -1.0, -1.0), (1.0, 1.0, 1.0)),
        label=f"monster_{k}",
        **kwargs,
    )
