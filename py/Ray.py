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
            origin (tuple[float, float, float]): Le point d'origine du rayon.
            direction (tuple[float, float, float]) :Le vecteur de direction du rayon.
        """
        self.origin = origin
        self.direction = direction

    def transform(self, T):
        """
        Transforme le rayon en un nouveau rayon selon une matrice donnée.

        Args:
            T (Transformation): Une transformation homogène.

        Returns:
            Ray: Un nouveau rayon dont l'origine et la direction ont été transformées.
        """

        (sx, sy, sz) = self.origin

        # w=1 car l'origine est un point (affecté par la translation)
        origin_mat = Matrix([[sx], [sy], [sz], [1]])

        (dx, dy, dz) = self.direction

        # w=0 car la direction est un vecteur (non affecté par la translation)
        direction_mat = Matrix([[dx], [dy], [dz], [0]])

        transformed_origin_mat = T.forward * origin_mat
        transformed_direction_mat = T.forward * direction_mat

        return Ray(
            transformed_origin_mat.to_tuple()[:3],
            transformed_direction_mat.to_tuple()[:3],
        )
