from Object import *
from AABB import AABB
from ObjectDAG import *


class WhitneyUmbrella(Prim):
    def __init__(self, color=None, T=None):
        bbox = AABB((-1, -1, -1), (1, 1, 1))
        super().__init__(WhitneyUmbrellaDAG(), color, T, None)


class Caylay(Prim):
    def __init__(self, color=None, T=None):
        super().__init__(CayleyDAG(), color, T, None)


class Plane(Prim):
    def __init__(self, color=None, T=None):

        super().__init__(PlaneDAG(), color, T, None)

    def intersection(self, ray):

        trf_ray = ray
        if self.T != None:
            trf_ray = ray.transform(~self.T)

        # if not self.bbox.intersection(trf_ray):
        #    return []

        sx, sy, sz = trf_ray.origin
        dx, dy, dz = trf_ray.direction

        denom = dz

        if abs(denom) < 1e-6:
            return []

        root = -sz / denom

        if root < 0.001:
            return []

        intervalles = []

        hit = self.compute_ray_hit(trf_ray, root)

        if self.T is not None:
            hit = self._local_to_world(hit, ray)

        intervalles.append(Intervalle(hit, hit))

        return intervalles

    def normale(self, x, y, z):
        return normalize3((0.0, 0.0, 1.0))


class Cylindre(Prim):
    def __init__(self, r, color=None, T=None):
        bbox = AABB(
            (-r, -r, -float("inf")),
            (r, r, float("inf")),
        )

        super().__init__(CylindreDAG(r), color, T, bbox)


class Sphere(Prim):
    def __init__(self, r, T=None, color=None):

        bbox = AABB(
            (-r, -r, -r),
            (r, r, r),
        )

        super().__init__(SphereDAG(r), color, T, bbox)


class Tore(Prim):
    def __init__(self, r, R, T=None, color=None):

        bbox = AABB((-r - R, -r, -r - R), (r + R, r, r + R))

        super().__init__(ToreDAG(r, R), color, T, bbox)


class Roman(Prim):
    def __init__(self, T=None, color=None):

        bbox = AABB((-1, -1, -1), (1, 1, 1))

        super().__init__(RomanDAG(), color, T, bbox)

    def _gradient(self, x, y, z):
        a = 2.0 * x * y * y + 2.0 * x * z * z - 2.0 * y * z
        b = 2.0 * y * x * x + 2.0 * y * z * z - 2.0 * x * z
        c = 2.0 * z * x * x + 2.0 * z * y * y - 2.0 * x * y

        return (a, b, c)

    def normale(self, x, y, z):

        (a, b, c) = self._gradient(x, y, z)

        return normalize3((a, b, c))


class Steiner2(Prim):
    def __init__(self, T=None, color=None):

        super().__init__(Steiner2DAG(), color, T, None)


class Steiner4(Prim):
    def __init__(self, T=None, color=None):

        super().__init__(Steiner4DAG(), color, T, None)


class HyperboloidTwoSheets(Prim):
    def __init__(self, T=None, color=None):

        super().__init__(HyperboloidTwoSheetsDAG(), color, T, None)


class HyperboloidOneSheet(Prim):
    def __init__(self, T=None, color=None):

        super().__init__(HyperboloidOneSheetDAG(), color, T, None)
