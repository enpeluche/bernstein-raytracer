from Matrix import Matrix
from Transformation import Transformation
from util import normalize3


class Ray:
    """
    Représentation mathématique d'un rayon lumineux.

    Un rayon est défini par une équation paramétrique de la forme :
    R(t) = source + t * direction, pour tout t appartenant à R.

    NOTE : Pour plus de détails, se réferer à la section 'Le rayon' du README.
    """

    __slots__ = ("origin", "direction")

    def __init__(
        self, origin: tuple[float, float, float], direction: tuple[float, float, float]
    ) -> None:
        """
        Initialise un nouveau rayon.

        Args:
            origin (tuple[float, float, float]): Le point d'origine du rayon.
            direction (tuple[float, float, float]) :Le vecteur de direction du rayon.
        """
        self.origin = origin
        self.direction = normalize3(direction)

    def transform(self, T: Transformation) -> "Ray":
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

        M = T.forward

        transformed_origin_mat = M * origin_mat
        transformed_direction_mat = M * direction_mat

        return Ray(
            transformed_origin_mat.to_tuple()[:3],
            transformed_direction_mat.to_tuple()[:3],
        )
