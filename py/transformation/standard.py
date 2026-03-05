from .base import Transformation

from math import cos, sin

# fmt: off
def translation(tx:float, ty:float, tz:float) -> Transformation:
    """
    Retourne une transformation qui effectue une translation de l'objet.

    Args:
        tx (float): Translation sur l'axe Ox.
        ty (float): Translation sur l'axe Oy.
        tz (float): Translation sur l'axe Oz.

    Returns:
        Transformation: La transformation correspondante (matrices forward et backward).
    """

    forward = [[1, 0, 0, tx],
               [0, 1, 0, ty],
               [0, 0, 1, tz],
               [0, 0, 0,  1]]
    
    backward = [[1, 0, 0, -tx],
                [0, 1, 0, -ty],
                [0, 0, 1, -tz],
                [0, 0, 0,   1]]

    return Transformation(forward, backward)


def rotation_x(θ: float) -> Transformation:
    """
    Retourne la transformation qui effectue une rotation de l'objet autour de l'axe x.

    Args:
        θ (float): Angle de rotation en radians.

    Returns:
        Transformation: La transformation correspondante (matrices forward et backward).
    """

    c, s = cos(θ), sin(θ)

    forward = [
        [1, 0,  0, 0],
        [0, c, -s, 0],
        [0, s,  c, 0],
        [0, 0,  0, 1],
    ]

    backward = [
        [1,  0, 0, 0],
        [0,  c, s, 0],
        [0, -s, c, 0],
        [0,  0, 0, 1],
    ]

    return Transformation(forward, backward)


def rotation_y(θ: float) -> Transformation:
    """
    Retourne la transformation qui effectue une rotation de l'objet autour de l'axe y.

    Args:
        θ (float): Angle de rotation en radians.

    Returns:
        Transformation: La transformation correspondante (matrices forward et backward).
    """

    c, s = cos(θ), sin(θ)

    forward = [
        [ c, 0, s, 0],
        [ 0, 1, 0, 0],
        [-s, 0, c, 0],
        [ 0, 0, 0, 1],
    ]
    backward = [
        [c, 0, -s, 0],
        [0, 1,  0, 0],
        [s, 0,  c, 0],
        [0, 0,  0, 1],
    ]

    return Transformation(forward, backward)


def rotation_z(θ: float) -> Transformation:
    """
    Retourne la transformation qui effectue une rotation de l'objet autour de l'axe z.

    Args:
        θ (float): Angle de rotation en radians.

    Returns:
        Transformation: La transformation correspondante (matrices forward et backward).
    """

    c, s = cos(θ), sin(θ)

    forward = [
        [c, -s, 0, 0],
        [s,  c, 0, 0],
        [0,  0, 1, 0],
        [0,  0, 0, 1],
    ]
    backward = [
        [ c, s, 0, 0],
        [-s, c, 0, 0],
        [ 0, 0, 1, 0],
        [ 0, 0, 0, 1],
    ]

    return Transformation(forward, backward)


def scaling(a: float, b: float, c: float) -> Transformation:
    """
    Retourne la transformation qui étire l'objet.

    Args:
        a (float): Facteur d'étirement sur l'axe Ox (doit être non nul).
        b (float): Facteur d'étirement sur l'axe Oy (doit être non nul).
        c (float): Facteur d'étirement sur l'axe Oz (doit être non nul).

    Raises:
        ValueError: Si a, b ou c est égal à 0.

    Returns:
        Transformation: La transformation correspondante (matrices forward et backward).
    """
    if a==0 or b==0 or c==0:
        raise ValueError(f"Impossible de créer une affinité avec un facteur nul (a:{a}, b:{b}, c:{c}).")

    forward = [
        [a, 0, 0, 0],
        [0, b, 0, 0],
        [0, 0, c, 0],
        [0, 0, 0, 1],
    ]
    backward = [
        [1 / a,     0,     0, 0],
        [    0, 1 / b,     0, 0],
        [    0,     0, 1 / c, 0],
        [    0,     0,     0, 1],
    ]

    return Transformation(forward, backward)

def identity() -> Transformation:
    """
    Retourne la transformation identité.

    Returns:
        Transformation: La transformation correspondante (matrices forward et backward).
    """
    I = [
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1],
    ]

    return Transformation(I, I)
# fmt: on
