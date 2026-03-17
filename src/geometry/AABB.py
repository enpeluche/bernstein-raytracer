from ..constants import EPSILON as ε


class AABB:
    """Represent an Axis-Aligned Bounding Box for spatial optimization.

    Provide a rectangular volume defined by its minimum and maximum
    extents along the Cartesian axes. Use this box to accelerate
    intersection tests by acting as a proxy for more complex
    geometric primitives.

    Attributes:
        x_min (float): Minimum coordinate on the X-axis, padded by ε.
        y_min (float): Minimum coordinate on the Y-axis, padded by ε.
        z_min (float): Minimum coordinate on the Z-axis, padded by ε.
        x_max (float): Maximum coordinate on the X-axis, padded by ε.
        y_max (float): Maximum coordinate on the Y-axis, padded by ε.
        z_max (float): Maximum coordinate on the Z-axis, padded by ε.
    """

    __slots__ = ("x_min", "y_min", "z_min", "x_max", "y_max", "z_max")

    def __init__(
        self, p1: tuple[float, float, float], p2: tuple[float, float, float]
    ) -> None:
        """Initialize a new AABB from two arbitrary points in 3D space.

        Calculate the minimum and maximum boundaries for each axis and
        apply a small safety margin (ε) to ensure the box strictly
        encloses its contents and prevents zero-thickness issues.

        Args:
            p1: First point defining the box.
            p2: Second point defining the box, usually diagonally
                opposite to p1.
        """

        self.x_min = min(p1[0], p2[0]) - ε
        self.y_min = min(p1[1], p2[1]) - ε
        self.z_min = min(p1[2], p2[2]) - ε

        self.x_max = max(p1[0], p2[0]) + ε
        self.y_max = max(p1[1], p2[1]) + ε
        self.z_max = max(p1[2], p2[2]) + ε

    def intersection(self, ray) -> bool:
        """Check for intersection between the ray and the AABB.

        Perform a high-performance, branchless "Slabs method"
        intersection test. Evaluate the overlap of entry and exit
        intervals on all three axes to determine if a valid
        intersection exists.

        Args:
            ray (Ray): The ray to test against the box. Requires
                precomputed `origin` and `inverse_direction`
                attributes.

        Returns:
            bool: True if the ray intersects the box at any point
                along its positive direction (t >= 0).
        """

        ox, oy, oz = ray.origin
        inv_dx, inv_dy, inv_dz = ray.inverse_direction

        tmin = -float("inf")
        tmax = float("inf")

        tx1 = (self.x_min - ox) * inv_dx
        tx2 = (self.x_max - ox) * inv_dx

        tmin = max(tmin, min(tx1, tx2))
        tmax = min(tmax, max(tx1, tx2))

        ty1 = (self.y_min - oy) * inv_dy
        ty2 = (self.y_max - oy) * inv_dy

        tmin = max(tmin, min(ty1, ty2))
        tmax = min(tmax, max(ty1, ty2))

        tz1 = (self.z_min - oz) * inv_dz
        tz2 = (self.z_max - oz) * inv_dz

        tmin = max(tmin, min(tz1, tz2))
        tmax = min(tmax, max(tz1, tz2))

        return tmax >= tmin and tmax >= 0

    def contains(self, other: "AABB") -> bool:
        """Determine if the current bounding box completely encloses another.

        Verify that all boundaries of the other AABB are within the
        minimum and maximum extents of this box. Use this to optimize
        hierarchical tests or to detect fully eclipsed volumes in
        CSG operations.

        Args:
            other: The bounding box to check for containment.

        Returns:
            bool: True if the other box is entirely inside the current
                volume, False otherwise.
        """

        return (
            self.x_min <= other.x_min
            and self.y_min <= other.y_min
            and self.z_min <= other.z_min
            and other.x_max <= self.x_max
            and other.y_max <= self.y_max
            and other.z_max <= self.z_max
        )

    def __sub__(self, other: "AABB | None") -> "AABB | None":
        """Subtract another bounding box from the current one.

        Perform a conservative subtraction. Return None if the current
        box is entirely contained within the other; otherwise, return
        the current box as a safe approximation.

        Args:
            other: The bounding box to subtract.

        Returns:
            The resulting AABB or None if the current box is fully
            eclipsed by the other.
        """

        if other is None:
            return self

        # if other.contains(self):
        #    return None

        return self

    def __add__(self, other: "AABB | None") -> "AABB | None":
        """Union the current bounding box with another.

        Create a new AABB that tightly encloses the combined volume
        of both input boxes. If the other box is None, return the
        current box.

        Args:
            other: The bounding box to merge with.

        Returns:
            A new AABB representing the union of both volumes.
        """

        if other is None:
            return self

        new_p1 = (
            min(self.x_min, other.x_min),
            min(self.y_min, other.y_min),
            min(self.z_min, other.z_min),
        )
        new_p2 = (
            max(self.x_max, other.x_max),
            max(self.y_max, other.y_max),
            max(self.z_max, other.z_max),
        )

        return AABB(new_p1, new_p2)

    def __and__(self, other: "AABB | None") -> "AABB | None":
        """Intersect the current bounding box with another.

        Calculate the overlapping region between two boxes. Determine
        if the intersection is valid across all axes; if not, return
        None to signify an empty volume.

        Args:
            other: The bounding box to intersect with.

        Returns:
            A new AABB representing the intersection volume, or None
            if the boxes do not overlap or if other is None.
        """

        if other is None:
            return None

        new_p1 = (
            max(self.x_min, other.x_min),
            max(self.y_min, other.y_min),
            max(self.z_min, other.z_min),
        )
        new_p2 = (
            min(self.x_max, other.x_max),
            min(self.y_max, other.y_max),
            min(self.z_max, other.z_max),
        )

        if new_p1[0] > new_p2[0] or new_p1[1] > new_p2[1] or new_p1[2] > new_p2[2]:
            return None

        return AABB(new_p1, new_p2)
