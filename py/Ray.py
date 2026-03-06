from Matrix import Matrix
from transformation import Transformation
from util import normalize3, dot3


class Ray:
    """
    Mathematical representation of a light ray.

    A ray is defined by a parametric equation of the form:
    $R(t) = \text{origin} + t \cdot \text{direction}$, for all $t \in \mathbb{R}$.

    NOTE: For more details, refer to the 'The Ray' section of the README.
    """

    __slots__ = (
        "origin",
        "direction",
        "norm_squared_origin",
        "norm_squared_direction",
        "dot",
        "env",
    )

    def __init__(
        self, origin: tuple[float, float, float], direction: tuple[float, float, float]
    ) -> None:
        """
        Initialize a new ray.

        Args:
            origin (tuple[float, float, float]): The ray's starting point (origin).
            direction (tuple[float, float, float]): The ray's direction vector.
        """
        self.origin = origin
        self.direction = normalize3(direction)

        self.norm_squared_origin = dot3(origin, origin)
        self.norm_squared_direction = 1.0  # la direction est normalisée
        self.dot = dot3(origin, self.direction)

        self.env = {
            "ox": origin[0],
            "oy": origin[1],
            "oz": origin[2],
            "dx": self.direction[0],
            "dy": self.direction[1],
            "dz": self.direction[2],
            "O2": self.norm_squared_origin,
            "D2": self.norm_squared_direction,
            "OD": self.dot,
        }

    def get_env(self) -> dict[str, float]:
        """
        Return the numerical environment mapping for the DAG evaluator.

        This mapping provides the actual float values for the ray's origin and
        direction components (e.g., 'ox', 'dx', etc.).
        """

        return self.env

    def _transform(self, T: Transformation) -> "Ray":
        """
        Transform the ray into a new coordinate system using a given matrix.

        Args:
            T (Transformation): A homogeneous transformation matrix.

        Returns:
            Ray: A new ray instance with its origin and direction transformed by T.
        """

        sx, sy, sz = self.origin

        # w=1 car l'origine est un point (affecté par la translation)
        origin_mat = Matrix._fast_create([[sx], [sy], [sz], [1]], 4, 1)

        dx, dy, dz = self.direction

        # w=0 car la direction est un vecteur (non affecté par la translation)
        direction_mat = Matrix._fast_create([[dx], [dy], [dz], [0]], 4, 1)

        M = T.forward

        transformed_origin_mat = M * origin_mat
        transformed_direction_mat = M * direction_mat

        return Ray(
            transformed_origin_mat.to_tuple()[:3],
            transformed_direction_mat.to_tuple()[:3],
        )

    def transform(self, T: Transformation) -> "Ray":

        ox, oy, oz = self.origin
        dx, dy, dz = self.direction

        M = T.forward

        # accès direct
        m = M.mat

        # origine
        ox2 = m[0][0] * ox + m[0][1] * oy + m[0][2] * oz + m[0][3]
        oy2 = m[1][0] * ox + m[1][1] * oy + m[1][2] * oz + m[1][3]
        oz2 = m[2][0] * ox + m[2][1] * oy + m[2][2] * oz + m[2][3]

        # direction
        dx2 = m[0][0] * dx + m[0][1] * dy + m[0][2] * dz
        dy2 = m[1][0] * dx + m[1][1] * dy + m[1][2] * dz
        dz2 = m[2][0] * dx + m[2][1] * dy + m[2][2] * dz

        return Ray((ox2, oy2, oz2), (dx2, dy2, dz2))
