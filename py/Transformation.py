from math import cos, sin
from Matrix import Matrix


class Transformation:
    def __init__(self, forward, backward):
        # Si 'forward' est déjà une Matrix, on la prend telle quelle.
        if isinstance(forward, Matrix):
            self.forward = forward
        else:
            # Sinon (c'est une liste), on la convertit.
            self.forward = Matrix(forward)

        # Pareil pour backward
        if isinstance(backward, Matrix):
            self.backward = backward
        else:
            self.backward = Matrix(backward)

    def __mul__(self, a):
        return Transformation(self.forward * a.forward, a.backward * self.backward)

    def __invert__(self):
        return Transformation(self.backward, self.forward)


# fmt: off
def translation(tx, ty, tz):

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
    I = [
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1],
    ]

    return Transformation(I, I)
# fmt: on
