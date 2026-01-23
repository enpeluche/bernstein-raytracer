class Ray(object):
    """
    Représentation mathématique d'un rayon lumineux.

    Un rayon est défini par une équation paramétrique de la forme :
    R(t) = source + t * direction, pour tout t appartenant à R.

    Note : Pour plus de détails, se réferer à la section 'Le rayon' du README.
    """

    def __init__(self, origin, direction):
        """
        Initialise un nouveau rayon.

        :param source: Un triplet (sx, sy, sz) de R^3 représentant le point d'origine du rayon.
        :param dir: Un triplet (dx, dy, dz) de R^3 représentant le vecteur de direction du rayon.
        """
        self.origin = origin
        self.direction = direction
