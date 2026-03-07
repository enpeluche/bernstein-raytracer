from transformation import *

# faire slots, cache


class GeometryObject:
    """Classe de base vide pour tous les objets de la scène."""

    __slots__ = ("aabb",)

    def intersection(self, ray):
        raise NotImplementedError

    def normal_at(self, x, y, z):
        raise NotImplementedError

    def transform(self, transformation):
        raise NotImplementedError

    def __add__(self, other) -> "GeometryObject":
        from .csg.union import Union

        return Union(self, other)

    def __sub__(self, other) -> "GeometryObject":
        from .csg.difference import Difference

        return Difference(self, other)

    def __and__(self, other) -> "GeometryObject":
        from .csg.intersection import Intersection

        return Intersection(self, other)

    def translate(self, tx: float, ty: float, tz: float) -> "GeometryObject":
        self.transform(translation(tx, ty, tz))

        return self

    def rotate_x(self, θ: float) -> "GeometryObject":
        self.transform(rotation_x(θ))

        return self

    def rotate_y(self, θ: float) -> "GeometryObject":
        self.transform(rotation_y(θ))

        return self

    def rotate_z(self, θ: float) -> "GeometryObject":
        self.transform(rotation_z(θ))

        return self

    def scale(self, sx: float, sy: float, sz: float) -> "GeometryObject":
        self.transform(scaling(sx, sy, sz))

        return self
