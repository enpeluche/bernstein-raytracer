from ..geometry import Primitive
from ..DAG import z
from ..Interval import Interval
from ..constants import EPSILON
from ..geometry.AABB import AABB

BIAS = 0.001


def plane(color=None, **kwargs) -> Primitive:
    """Helper for a simple infinite plane at z=0."""
    return HalfSpace(color=color, **kwargs)


class HalfSpace(Primitive):
    """
    Represents an infinite half-space (z <= 0).
    Perfect for capping infinite cylinders or slicing objects via CSG.
    """

    def __init__(self, color=None, **kwargs):
        # We define an AABB that is infinite in X, Y and negative Z
        inf_aabb = AABB(
            (-float("inf"), -float("inf"), -float("inf")),
            (float("inf"), float("inf"), 0.0),
        )

        super().__init__(
            implicit_function=z,  # On passe directement le noeud DAG
            color=color,
            aabb=inf_aabb,
            label="half_space",
            **kwargs
        )

    def intersection(self, ray):  # Renommé pour la cohérence CSG
        """Computes the intersection between a ray and the half-space z <= 0."""

        # 1. Coordinate space transformation
        local_ray = ray.transform(~self.transformation) if self.transformation else ray

        _, _, oz = local_ray.origin
        _, _, dz = local_ray.direction

        # 2. Ray range from the ray itself
        t_start = ray.t_min
        t_end = ray.t_max

        # 3. Solve the linear inequality: oz + t * dz <= 0
        if abs(dz) < EPSILON:  # Ray is parallel to the XY plane
            if oz > 0:
                return []  # Entirely outside (above the plane)
            # Else: Entirely inside (keep the full ray range)
        else:
            t_hit = -oz / dz
            if dz > 0:
                # Ray is pointing UP: it exits the matter at t_hit
                t_end = min(t_end, t_hit)
            else:
                # Ray is pointing DOWN: it enters the matter at t_hit
                t_start = max(t_start, t_hit)

        # 4. Final validation
        if t_start > t_end or t_end < BIAS:
            return []

        # 5. Return the interval trapped in the half-space
        hit_in = self.evaluate_hit(local_ray, t_start)
        hit_out = self.evaluate_hit(local_ray, t_end)

        return [Interval(hit_in, hit_out)]
