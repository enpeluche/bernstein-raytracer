from DAG import *

x = Var("x")
y = Var("y")
z = Var("z")


def boule(cx, cy, cz, r):
    return (
        (x - Nb(cx)) * (x - Nb(cx))
        + (y - Nb(cy)) * (y - Nb(cy))
        + (z - Nb(cz)) * (z - Nb(cz))
        - Nb(r) * Nb(r)
    )


def tore(r, R):
    tmp = x * x + y * y + z * z + Nb(R * R - r * r)

    return tmp * tmp - Nb(4.0 * R * R) * (x * x + z * z)


def steiner2():
    return x * x * y * y - x * x * z * z + y * y * z * z - x * y * z


def steiner4():
    return (
        y * y
        - Nb(2.0) * x * y * y
        - x * z * z
        + x * x * y * y
        + x * x * z * z
        - z * z * z * z
    )


def hyperboloide_2nappes():
    return Nb(0.0) - (z * z - (x * x + y * y + Nb(0.1)))


def hyperboloide_1nappe():
    return Nb(0.0) - (z * z - (x * x + y * y - Nb(0.1)))


def roman():
    return x * x * y * y + x * x * z * z + y * y * z * z - Nb(2.0) * x * y * z
