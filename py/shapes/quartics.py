from geometry import Primitive
from DAG import x, y, z
from geometry import AABB


def steiner2(color=None, **kwargs) -> Primitive:

    return Primitive(
        implicit_function=x ** 2 * y ** 2
        - x ** 2 * z ** 2
        + y ** 2 * z ** 2
        - x * y * z,
        color=color,
        label="steiner2",
        **kwargs,
    )


def steiner4(color=None, **kwargs) -> Primitive:

    return Primitive(
        implicit_function=y ** 2
        - 2.0 * x * y ** 2
        - x * z ** 2
        + x ** 2 * y ** 2
        + x ** 2 * z ** 2
        - z ** 4,
        color=color,
        label="steiner4",
        **kwargs,
    )


def roman(color=None, **kwargs) -> Primitive:

    return Primitive(
        implicit_function=x ** 2 * y ** 2
        + x ** 2 * z ** 2
        + y ** 2 * z ** 2
        - 2.0 * x * y * z,
        color=color,
        aabb=AABB((-1, -1, -1), (1, 1, 1)),
        label="roman",
        **kwargs,
    )


def torus(R: float = 0.7, r: float = 0.3, color=None, **kwargs) -> Primitive:

    R2 = R * R
    r2 = r * r

    quadric = x ** 2 + y ** 2 + z ** 2 + R2 - r2

    return Primitive(
        implicit_function=quadric ** 2 - 4.0 * R2 * (x ** 2 + z ** 2),
        color=color,
        aabb=AABB((-r - R, -r, -r - R), (r + R, r, r + R)),
        label="torus",
        **kwargs,
    )
