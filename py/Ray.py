from transformation import Transformation
from util import normalize3, dot3
from constants import EPSILON


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
        "inverse_direction",
        "norm_squared_origin",
        "norm_squared_direction",
        "dot",
        "eval_params",
        "t_min",
        "t_max",
    )

    def __init__(
        self,
        origin: tuple[float, float, float],
        direction: tuple[float, float, float],
        should_normalize: bool = True,
        t_min: float = EPSILON,
        t_max: float = float("inf"),
    ) -> None:
        """
        Initialize a new ray.

        Args:
            origin (tuple[float, float, float]): The ray's starting point (origin).
            direction (tuple[float, float, float]): The ray's direction vector.
            should_normalize (bool): If True, normalizes the direction vector
            t_min (float): The minimum valid intersection distance. Used to prevent self-intersection artifacts (shadow acne).
            t_max (float): The maximum valid intersection distance. Used to limit the ray's reach (e.g., stopping at a light source).
        """
        self.t_min = t_min
        self.t_max = t_max

        self.origin = origin

        if should_normalize:
            self.direction = normalize3(direction)
            self.norm_squared_direction = 1.0
        else:
            self.direction = direction
            self.norm_squared_direction = dot3(direction, direction)

        dx, dy, dz = self.direction
        self.inverse_direction = (
            1.0 / dx if dx != 0 else float("inf"),
            1.0 / dy if dy != 0 else float("inf"),
            1.0 / dz if dz != 0 else float("inf"),
        )

        self.norm_squared_origin = dot3(origin, origin)

        self.dot = dot3(origin, self.direction)

        self.eval_params = (
            origin[0],
            origin[1],
            origin[2],
            self.direction[0],
            self.direction[1],
            self.direction[2],
            self.norm_squared_origin,
            self.norm_squared_direction,
            self.dot,
        )

    def transform(self, transformation: Transformation) -> "Ray":
        """
        Transform the ray into a new coordinate system using a given matrix.

        Args:
            transformation (Transformation): A homogeneous transformation matrix.

        Returns:
            Ray: A new ray instance with its origin and direction transformed by transformation.
        """

        ox, oy, oz = self.origin
        dx, dy, dz = self.direction

        m = transformation.forward.mat

        # transformed origin
        ox2 = m[0][0] * ox + m[0][1] * oy + m[0][2] * oz + m[0][3]
        oy2 = m[1][0] * ox + m[1][1] * oy + m[1][2] * oz + m[1][3]
        oz2 = m[2][0] * ox + m[2][1] * oy + m[2][2] * oz + m[2][3]

        # transformed direction
        dx2 = m[0][0] * dx + m[0][1] * dy + m[0][2] * dz
        dy2 = m[1][0] * dx + m[1][1] * dy + m[1][2] * dz
        dz2 = m[2][0] * dx + m[2][1] * dy + m[2][2] * dz

        return Ray(
            origin=(ox2, oy2, oz2),
            direction=(dx2, dy2, dz2),
            should_normalize=False,
            t_min=self.t_min,
            t_max=self.t_max,
        )
