from Matrix import Matrix


class Ray:
    """
    Représentation mathématique d'un rayon lumineux.

    Un rayon est défini par une équation paramétrique de la forme :
    R(t) = source + t * direction, pour tout t appartenant à R.

    Note : Pour plus de détails, se réferer à la section 'Le rayon' du README.
    """

    def __init__(self, origin, direction):
        """
        Initialise un nouveau rayon.

        Args:
            source (tuple[float, float, float]): Le point d'origine du rayon.
            dir (tuple[float, float, float]) :Le vecteur de direction du rayon.
        """
        self.origin = origin
        self.direction = direction

    def transform(self, T):
        """
        Transforme le rayon en un nouveau rayon.

        Args:
            T (Transformation): Une transformation homogène.
        """

        (sx, sy, sz) = self.origin
        origin_mat = Matrix([[sx], [sy], [sz], [1]])

        (dx, dy, dz) = self.direction
        direction_mat = Matrix([[dx], [dy], [dz], [0]])

        transformed_origin_mat = T.forward * origin_mat
        transformed_direction_mat = T.forward * direction_mat

        return Ray(
            transformed_origin_mat.to_tuple()[:3],
            transformed_direction_mat.to_tuple()[:3],
        )
