class AABB:
    """
    AABB est l'acronyme de "Axis-Aligned Bounding box".

    TODO : Il faut tester les AABB d'épaisseurs nuls.
    """

    __slots__ = ("bounds_start", "bounds_end")

    def __init__(self, p1, p2):
        """
        Créer une AABB, utile pour diminuer le temps de calcul.

        Il n'y a pas d'ordre total sur R^3 mais on suppose que
        bounds_start_i < bounds_end_i pour tout i.

        Args:
            p1 (tuple[float, float, float]): La coordonnée de début de la AABB.
            p2 (tuple[float, float, float]): La coordonnée de fin de la AABB.
        """

        self.bounds_start = (min(p1[0], p2[0]), min(p1[1], p2[1]), min(p1[2], p2[2]))

        self.bounds_end = (max(p1[0], p2[0]), max(p1[1], p2[1]), max(p1[2], p2[2]))

    def intersection(self, ray):
        """
        Test l'intersection entre elle-même et un rayon. Implémentation de l'algorithme de "Slabs methods".

        Args:
            ray (Ray): Un rayon.

        Returns:
            A boolean
        """

        (sx, sy, sz) = ray.origin
        (dx, dy, dz) = ray.direction

        tmin = -float("inf")
        tmax = float("inf")

        if dx != 0:
            tx1 = (self.bounds_start[0] - sx) / dx
            tx2 = (self.bounds_end[0] - sx) / dx

            tmin = max(tmin, min(tx1, tx2))
            tmax = min(tmax, max(tx1, tx2))

        elif sx < self.bounds_start[0] or sx > self.bounds_end[0]:
            return False

        if dy != 0:
            ty1 = (self.bounds_start[1] - sy) / dy
            ty2 = (self.bounds_end[1] - sy) / dy

            tmin = max(tmin, min(ty1, ty2))
            tmax = min(tmax, max(ty1, ty2))

        elif sy < self.bounds_start[1] or sy > self.bounds_end[1]:
            return False

        if dz != 0:
            tz1 = (self.bounds_start[2] - sz) / dz
            tz2 = (self.bounds_end[2] - sz) / dz

            tmin = max(tmin, min(tz1, tz2))
            tmax = min(tmax, max(tz1, tz2))

        elif sz < self.bounds_start[2] or sz > self.bounds_end[2]:
            return False

        return tmax >= tmin and tmax >= 0
