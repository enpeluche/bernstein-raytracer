from geometry import Primitive
from DAG import z
from Interval import Interval
from constants import EPSILON

bias = 0.001


def plane(color, **kwargs):
    return Primitive(implicit_function=z, color=color, label="plane", **kwargs)


class HalfSpace(Primitive):
    """
    Represents an infinite half-space.
    By default, the half-space is defined at z < 0 (XY-half-space).
    """

    def __init__(self, color=None, show_grid=False):
        from DAG import plane_implicit_function

        # Initialize the primitive with its specific DAG node and properties
        # we use PlaneDAG since normal is the same
        super().__init__(
            implicit_function=plane_implicit_function(),
            color=color,
            dual_color=True,
            show_grid=show_grid,
            bbox=None,
        )

    def intersect(self, ray):
        """
        Computes the intersection between a ray and the half-space.
        Solves the linear equation: oz + t * dz <= 0
        """

        # 1. Transform ray from world space to local space
        trf_ray = ray

        if self.transformation is not None:
            trf_ray = ray.transform(~self.transformation)

        # 2. Extract Z components (since plane is at z=0)
        _, _, oz = trf_ray.origin
        _, _, dz = trf_ray.direction

        # 3. Initialize the default interval for a semi-infinite volume
        t_start = 0.0
        t_end = float("inf")

        # 4. Solve the linear inequality: oz + t * dz <= 0

        if abs(dz) < EPSILON:  # Case: Ray is parallel to the plane
            if oz > 0:
                return []  # Ray is entirely outside
            # Else: Ray is entirely inside (keep [0, inf])

        elif dz >= EPSILON:  # Case : Ray points UP (exiting the volume)
            t_root = -oz / dz
            t_end = min(t_end, t_root)

        else:  # Case : Ray points DOWN (entering the volume)
            t_root = -oz / dz
            t_start = max(t_start, t_root)

        # 5. Final check: if the interval is invalid or entirely behind the camera
        if t_start > t_end or t_end < bias:
            return []

        # 6. Build Hit Records
        # Note: t_start can be 0.0 if we start inside
        # hit_a and hit_b represent the segment of the ray trapped in the matter

        hit_a = self.evaluate_hit(trf_ray, t_start)
        hit_b = self.evaluate_hit(trf_ray, t_end)

        if self.transformation is not None:
            hit_a = self._local_to_world(hit_a, ray)
            hit_b = self._local_to_world(hit_b, ray)

        return [Interval(hit_a, hit_b)]
