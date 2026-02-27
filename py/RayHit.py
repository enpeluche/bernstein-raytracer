class RayHit:
    """
    Contient toutes les informations géométriques et visuelles d'un point d'impact
    entre un rayon et une surface géométrique.
    """

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
        Initialise un nouveau point d'impact.

        Args:
            t (float): Moment t de l'impact (distance le long du rayon).
            pt (tuple[float, float, float]): Coordonnées 3D globales de l'impact (x, y, z).
            local_pt (tuple[float, float]): Point d'impact en coordonnées locales UV (u, v).
            plan (tuple[float, float, float, float]): Plan tangent à l'impact (nx, ny, nz, d).
            color (tuple[int, int, int]): Couleur RGB du point d'impact.
            apply_face_color (bool): Indique si on doit appliquer la couleur de la face.
            apply_grid_pattern (bool): Indique si on doit appliquer la texture procédurale quadrillée.
        """

        self.t = t
        self.pt = pt
        self.local_pt = local_pt
        self.plan = plan
        self.color = color
        self.apply_face_color = apply_face_color
        self.apply_grid_pattern = apply_grid_pattern

    def __repr__(self):
        """Représentation textuelle de l'impact pour le débogage."""
        return f"RayHit(t={self.t:.3f} pt={self.pt[0]:.3f}, {self.pt[1]:.3f}, {self.pt[2]:.3f}, plan={self.plan[0]:.3f}, {self.plan[1]:.3f}, {self.plan[2]:.3f}, color={self.color})"
