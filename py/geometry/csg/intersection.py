from .base import CSGNode
from Csg1D import inter


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
