from .base import CSGNode
from Csg1D import differ


class Difference(CSGNode):
    """Nœud CSG représentant la soustraction (différence)."""

    __slots__ = ()

    def __init__(self, left, right) -> None:
        super().__init__(left, right)

        self.aabb = left.aabb - right.aabb

    def intersection(self, ray):
        if not self.aabb.intersection(ray):
            return []

        return differ(self.left.intersection(ray), self.right.intersection(ray))
