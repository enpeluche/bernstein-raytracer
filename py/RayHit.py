class RayHit:
    """
    Store geometric and visual attributes of a ray-surface intersection.

    This class serves as a data container for all properties derived during
    the intersection process, facilitating coordinate transformations and
    shading calculations between local and parent spaces.
    """

    __slots__ = (
        "primitive",
        "impact_time",
        "local_impact_point",
        "world_impact_point",
        "local_normal",
        "world_normal",
        "is_front_face",
    )

    def __init__(
        self,
        primitive,
        impact_time: float,
        local_impact_point: tuple[float, float, float],
        world_impact_point: tuple[float, float, float],
        local_normal: tuple[float, float, float],
        world_normal: tuple[float, float, float],
        is_front_face: bool,
    ) -> None:
        """Initialize a new ray-surface intersection record.

        Args:
            primitive (Primitive): The geometric object intersected by the ray.
            impact_time (float): The distance along the ray to the hit point ($t$).
            local_impact_point (tuple[float, float, float]): The 3D coordinates of the impact in the object's local coordinate system.
            world_impact_point (tuple[float, float, float]): The 3D coordinates of the impact in the parent or world coordinate system.
            local_normal (tuple[float, float, float]): The surface normal vector at the impact point in local coordinates.
            world_normal (tuple[float, float, float]): The surface normal vector at the impact point in parent or world coordinates.
            is_front_face (bool): True if the ray hit the surface from the outside, False if it hit the interior face.
        """
        self.primitive = primitive
        self.impact_time = impact_time
        self.local_impact_point = local_impact_point
        self.world_impact_point = world_impact_point
        self.local_normal = local_normal
        self.world_normal = world_normal
        self.is_front_face = is_front_face

    def invert(self) -> None:
        """Inverse la normale et l'orientation de la face (utile pour la CSG)."""
        # Inversion des vecteurs
        self.local_normal = (
            -self.local_normal[0],
            -self.local_normal[1],
            -self.local_normal[2],
        )
        self.world_normal = (
            -self.world_normal[0],
            -self.world_normal[1],
            -self.world_normal[2],
        )

        # Une face avant devient une face arrière et vice-versa
        self.is_front_face = not self.is_front_face

    def __repr__(self) -> str:
        """Return a formatted string representation for debugging.

        Returns:
            str: A concise summary of the hit including face orientation,
                impact time, parent coordinates, and normal vector.
        """
        face = "Front" if self.is_front_face else "Back"
        px, py, pz = self.world_impact_point
        nx, ny, nz = self.world_normal

        return (
            f"RayHit(face={face}, time={self.impact_time:.3f}, "
            f"pos=({px:.3f}, {py:.3f}, {pz:.3f}), "
            f"norm=({nx:.3f}, {ny:.3f}, {nz:.3f}), "
            f"color={self.primitive.color})"
        )
