from math import cos, sin
from Matrix import Matrix


class Transformation:
    """
    Représente une transformation de l'espace, contenant la transformation dans un sens, et dans le sens inverse.
    """

    def __init__(self, forward, backward):
        """
        Args:
            forward (Matrix or tuple[tuple]): La matrice de la transformation (doit être inversible).
            backward (Matrix or tuple[tuple]): La matrice inverse pré-calculée de 'forward'.
        """
        if isinstance(forward, Matrix):
            self.forward = forward
        else:
            self.forward = Matrix(forward)

        if isinstance(backward, Matrix):
            self.backward = backward
        else:
            self.backward = Matrix(backward)

    def __mul__(self, a):
        """
        Surcharge de l'opérateur *.
        Renvoie la transformation résultante d'effectuer la transformation a puis la transformation self.

        Args:
            a (Transformation)
        """
        return Transformation(self.forward * a.forward, a.backward * self.backward)

    def __invert__(self):
        """
        Surcharge de l'opérateur ~.
        Retourne sa transformation inverse.
        """
        return Transformation(self.backward, self.forward)


# fmt: off
def translation(tx, ty, tz):
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


def rotation_x(θ):
    """
    Retourne la transformation qui effectue une rotation de l'objet autour de l'axe x.

    Args:
        θ (float): Angle de rotation en radians.

    Returns:
        Transformation: La transformation correspondante (matrices forward et backward).
    """

    forward = [
        [1,      0,       0, 0],
        [0, cos(θ), -sin(θ), 0],
        [0, sin(θ),  cos(θ), 0],
        [0,       0,      0, 1],
    ]

    backward = [
        [1,       0,      0, 0],
        [0,  cos(θ), sin(θ), 0],
        [0, -sin(θ), cos(θ), 0],
        [0,       0,      0, 1],
    ]

    return Transformation(forward, backward)


def rotation_y(θ):
    """
    Retourne la transformation qui effectue une rotation de l'objet autour de l'axe y.

    Args:
        θ (float): Angle de rotation en radians.

    Returns:
        Transformation: La transformation correspondante (matrices forward et backward).
    """

    forward = [
        [ cos(θ), 0, sin(θ), 0],
        [      0, 1,      0, 0],
        [-sin(θ), 0, cos(θ), 0],
        [      0, 0,      0, 1],
    ]
    backward = [
        [cos(θ), 0, -sin(θ), 0],
        [     0, 1,       0, 0],
        [sin(θ), 0,  cos(θ), 0],
        [     0, 0,       0, 1],
    ]

    return Transformation(forward, backward)


def rotation_z(θ):
    """
    Retourne la transformation qui effectue une rotation de l'objet autour de l'axe z.

    Args:
        θ (float): Angle de rotation en radians.

    Returns:
        Transformation: La transformation correspondante (matrices forward et backward).
    """

    forward = [
        [cos(θ), -sin(θ), 0, 0],
        [sin(θ),  cos(θ), 0, 0],
        [     0,       0, 1, 0],
        [     0,       0, 0, 1],
    ]
    backward = [
        [ cos(θ), sin(θ), 0, 0],
        [-sin(θ), cos(θ), 0, 0],
        [      0,      0, 1, 0],
        [      0,      0, 0, 1],
    ]

    return Transformation(forward, backward)


def scaling(a, b, c):
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

def identity():
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
