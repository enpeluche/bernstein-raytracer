from math import sqrt
from random import randint
from .constants import EPSILON


def norm3(v: tuple[float, float, float]) -> float:

    """
    Compute the Euclidean norm ($L_2$) of a 3D vector.

    This value represents the geometric length of the vector in 3D space.
    Refer to the project's documentation for further mathematical details.

    Args:
        v (tuple[float, float, float]): The 3D vector $(x, y, z)$.

    Returns:
        float: The magnitude of the vector, calculated as $\sqrt{v_x^2 + v_y^2 + v_z^2}$.
    """

    (vx, vy, vz) = v

    return sqrt(vx * vx + vy * vy + vz * vz)


def dot3(u: tuple[float, float, float], v: tuple[float, float, float]) -> float:

    """
    Compute the dot product of two 3D vectors.

    The dot product is foundational for determining the angle between vectors
    or for projections. It is the cornerstone of lighting calculations
    (e.g., Lambert's Cosine Law).

    Args:
        u (tuple[float, float, float]): The first 3D vector.
        v (tuple[float, float, float]): The second 3D vector.

    Returns:
        float: The scalar result ($u_x v_x + u_y v_y + u_z v_z$).
    """

    (ux, uy, uz) = u
    (vx, vy, vz) = v

    return ux * vx + uy * vy + uz * vz


def normalize3(v: tuple[float, float, float]) -> tuple[float, float, float]:

    """
    Scale a 3D vector to a unit length of 1.

    This operation is crucial for direction vectors (like rays or normals).
    If the vector's norm is near zero (below EPSILON), a zero vector is returned
    to prevent division by zero errors.

    Args:
        v (tuple[float, float, float]): The vector to normalize.

    Returns:
        tuple[float, float, float]: A unit vector in the same direction, or (0,0,0).
    """

    norm = norm3(v)

    if norm < EPSILON:
        return (0.0, 0.0, 0.0)
    else:
        return (v[0] / norm, v[1] / norm, v[2] / norm)


# NOTE to clamp : verouiller
def clamp(m: float, M: float, x: float) -> float:

    """
    Clamp the value x to the interval [m, M].

    This utility ensures the value remains within the specified bounds.
    Refer to the README for further details.

    Args:
        m (float): The lower bound.
        M (float): The upper bound.
        x (float): The value to restrict.

    Returns:
        float: The clamped value such that $m \le x \le M$.
    """
    return min(M, max(m, x))


def lerp(x1: float, y1: float, x2: float, y2: float, x: float) -> float:

    """
    Compute the linear interpolation (LERP) of x between two control points.

    This function utilizes the Lagrange form of a first-degree polynomial
    to map a value from a source interval $[x_1, x_2]$ to a target interval $[y_1, y_2]$.

    Refer to the README for further mathematical context.

    Args:
        x1 (float): Abscissa of the first control point.
        y1 (float): Ordinate of the first control point (target value).
        x2 (float): Abscissa of the second control point.
        y2 (float): Ordinate of the second control point (target value).
        x (float): The input value to be interpolated.

    Returns:
        float: The interpolated value $y$ corresponding to $x$.
    """
    x1, y1, x2, y2, x = float(x1), float(y1), float(x2), float(y2), float(x)

    assert x1 != x2

    return ((x - x2) / (x1 - x2)) * y1 + ((x - x1) / (x2 - x1)) * y2


def cross(
    u: tuple[float, float, float], v: tuple[float, float, float]
) -> tuple[float, float, float]:

    """
    Compute the cross product of two 3D vectors.

    The cross product yields a third vector that is perpendicular (orthogonal)
    to the plane formed by u and v. This operation is essential in raytracing
    for calculating surface normals and constructing local coordinate systems.

    Refer to the README for further mathematical details.

    Args:
        u (tuple[float, float, float]): The first 3D vector.
        v (tuple[float, float, float]): The second 3D vector.

    Returns:
        tuple[float, float, float]: The resulting orthogonal vector $w$.
    """
    u0, u1, u2 = u
    v0, v1, v2 = v

    return (u1 * v2 - u2 * v1, u2 * v0 - u0 * v2, u0 * v1 - u1 * v0)


def random_color() -> tuple[int, int, int]:
    """
    Generate a random RGB color tuple.

    The function produces three random 8-bit integers representing
    the Red, Green, and Blue channels of a color.

    Returns:
        tuple[int, int, int]: A tuple $(R, G, B)$ where each component is in $[0, 255]$.
    """
    return (randint(0, 255), randint(0, 255), randint(0, 255))
