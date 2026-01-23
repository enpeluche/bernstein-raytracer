import math


def normalize3(v):
    """
    Normalise un vecteur 3D pour lui donner une longueur de 1.

    Args:
        v (tuple): Un tuple de 3 flottants représentant le vecteur.

    Returns:
        tuple: Un nouveau tuple de même direction mais de norme 1.
    """

    (vx, vy, vz) = v

    norm = math.sqrt(vx * vx + vy * vy + vz * vz)

    if 0.0 == norm:
        return (0.0, 0.0, 0.0)
    else:
        return (vx / norm, vy / norm, vz / norm)


# NOTE to clamp : verouiller
def clamp(m, M, x):
    """
    Restreint v à l'intervalle [m, M].

    Args:
        m (float): La borne inférieure.
        M (float): La borne supérieure.
        x (float): La valeur à restreindre.

    Returns:
        float: La valeur bridée tel que m <= x <= M.
    """
    return min(M, max(m, x))


def interpole(x1, y1, x2, y2, x):
    """
    Calcul l'image de x par interpolation linéaire entre deux points.

    Cette fonction utilise la forme de Lagrange pour un polynôme de degré 1
    afin de projeter la valeur d'un intervalle source vers un intervalle cible.

    Args:
        x1 (float): Abscisse du premier point de contrôle.
        y1 (float): Ordonnée du premier point de contrôle (valeur cible).
        x2 (float): Abscisse du second point de contrôle.
        y2 (float): Ordonnée du second point de contrôle (valeur cible).
        x (float): La valeur à interpoler.

    Returns:
        float: La valeur interpolée y correspondant à x.
    """
    x1, y1, x2, y2, x = float(x1), float(y1), float(x2), float(y2), float(x)

    return ((x - x2) / (x1 - x2)) * y1 + ((x - x1) / (x2 - x1)) * y2
