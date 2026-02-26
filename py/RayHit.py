class RayHit:
    """ """

    __slots__ = (
        "t",
        "pt",
        "local_pt",
        "plan",
        "color",
        "apply_face_color",
        "apply_grid_pattern",
    )

    def __init__(
        self, t, pt, local_pt, plan, color, apply_face_color, apply_grid_pattern
    ):
        """

        Args:
            t (float): Moment t de l'impact.
            pt tuple[float]: Coordonnées de l'impact.
            plan tuple[float]: Plan tangeant de l'impact
            color tuple[float]: Couleur du point d'impact
        """
        self.t = t
        self.pt = pt
        self.local_pt = local_pt
        self.plan = plan
        self.color = color
        self.apply_face_color = apply_face_color
        self.apply_grid_pattern = apply_grid_pattern

    def __repr__(self):
        return f"RayHit(t={self.t:.3f} pt={self.pt[0]:.3f}, {self.pt[1]:.3f}, {self.pt[2]:.3f}, plan={self.plan[0]:.3f}, {self.plan[1]:.3f}, {self.plan[2]:.3f}, color={self.color})\n"
