from .base import CSGNode
from ...Csg1D import differ


class Difference(CSGNode):
    """Nœud CSG représentant la soustraction (différence)."""

    __slots__ = ()

    def __init__(self, left, right) -> None:
        super().__init__(left, right)

        self.aabb = left.aabb - right.aabb

    def _intersection(self, ray, debug=False):
        if not self.aabb.intersection(ray):
            return []

        return differ(self.left.intersection(ray), self.right.intersection(ray))

    def intersection(self, ray, debug=False):
        if self.aabb is not None and not self.aabb.intersection(ray):
            return []

        left_intervals = self.left.intersection(ray)
        right_intervals = self.right.intersection(ray)

        for interval in right_intervals:
            interval.hit_in.invert()
            interval.hit_out.invert()

        return differ(left_intervals, right_intervals)

    def any_intersection(self, ray) -> bool:
        if self.aabb is not None and not self.aabb.intersection(ray):
            return False

        # Si le côté gauche (l'objet principal) ne touche pas, c'est fini.
        if not self.left.any_intersection(ray):
            return False

        # Si la gauche touche mais que la droite ne touche pas du tout,
        # alors la différence touche forcément.
        if not self.right.any_intersection(ray):
            return True

        # Si les deux touchent, on doit vérifier si la droite ne "mange" pas
        # toute la gauche.
        return bool(self.intersection(ray))
