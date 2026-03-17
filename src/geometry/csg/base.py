from ..base import GeometryObject


class CSGNode(GeometryObject):
    __slots__ = ("left", "right")

    def __init__(self, left, right) -> None:
        self.left = left
        self.right = right
        self.aabb = None

    def transform(self, transformation):
        self.left.transform(transformation)
        self.right.transform(transformation)

        return self
