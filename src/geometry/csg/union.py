from .base import CSGNode
from ...Csg1D import union


class Union(CSGNode):
    """Nœud CSG représentant l'union (addition)."""

    __slots__ = ()

    def __init__(self, left, right) -> None:
        super().__init__(left, right)

        self.aabb = left.aabb + right.aabb

    def intersection(self, ray):
        if not self.aabb.intersection(ray):
            return []

        return union(self.left.intersection(ray), self.right.intersection(ray))

    def any_intersection(self, ray) -> bool:
        if not self.aabb.intersection(ray):
            return False

        # Court-circuit : si le gauche touche, on n'évalue même pas le droit.
        return self.left.any_intersection(ray) or self.right.any_intersection(ray)
