from .base import CSGNode
from ...Csg1D import inter


class Intersection(CSGNode):
    """Nœud CSG représentant l'intersection."""

    __slots__ = ()

    def __init__(self, left, right) -> None:
        super().__init__(left, right)

        self.aabb = left.aabb & right.aabb

    def intersection(self, ray):
        if not self.aabb.intersection(ray):
            return []

        return inter(self.left.intersection(ray), self.right.intersection(ray))

    def any_intersection(self, ray) -> bool:
        if not self.aabb.intersection(ray):
            return False

        # On vérifie d'abord si les deux touchent individuellement (rapide)
        if not self.left.any_intersection(ray) or not self.right.any_intersection(ray):
            return False

        # Si les deux touchent, on est obligé de calculer les intervalles réels
        # pour vérifier s'ils se chevauchent.
        return bool(self.intersection(ray))
