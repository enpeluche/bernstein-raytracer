from Matrix import Matrix


class RayHit:
    """ """

    __slots__ = ("t", "pt", "plan", "color")

    def __init__(self, t, pt, plan, color):
        """

        Args:
            t (float): Moment t de l'impact.
            pt tuple[float]: Coordonnées de l'impact.
            plan tuple[float]: Plan tangeant de l'impact
            color tuple[float]: Couleur du point d'impact
        """
        self.t = t
        self.pt = pt
        self.plan = plan
        self.color = color

    def __repr__(self):
        return f"RayHit(t={self.t:.3f} pt={self.pt[0]:.3f}, {self.pt[1]:.3f}, {self.pt[2]:.3f}, plan={self.plan[0]:.3f}, {self.plan[1]:.3f}, {self.plan[2]:.3f}, color={self.color})\n"
