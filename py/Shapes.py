from Object import *
from AABB import AABB
from ObjectDAG import *


class WhitneyUmbrella(Prim):
    def __init__(self, color=None, T=None, apply_grid_pattern=False):
        bbox = AABB((-1, -1, -1), (1, 1, 1))
        super().__init__(WhitneyUmbrellaDAG(), color, True, apply_grid_pattern, T, None)


class Caylay(Prim):
    def __init__(self, color=None, T=None, apply_grid_pattern=False):
        super().__init__(CayleyDAG(), color, True, apply_grid_pattern, T, None)


class Plane(Prim):
    def __init__(self, color=None, T=None, apply_grid_pattern=False):

        super().__init__(PlaneDAG(), color, True, apply_grid_pattern, T, None)

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
    def __init__(self, r, color=None, T=None, apply_grid_pattern=False):
        bbox = AABB(
            (-r, -r, -float("inf")),
            (r, r, float("inf")),
        )

        super().__init__(CylindreDAG(r), color, True, apply_grid_pattern, T, bbox)


class Sphere(Prim):
    def __init__(self, r, T=None, color=None, apply_grid_pattern=False):

        bbox = AABB(
            (-r, -r, -r),
            (r, r, r),
        )

        super().__init__(SphereDAG(r), color, True, apply_grid_pattern, T, bbox)


class Tore(Prim):
    def __init__(self, r, R, T=None, color=None, apply_grid_pattern=False):

        bbox = AABB((-r - R, -r, -r - R), (r + R, r, r + R))

        super().__init__(ToreDAG(r, R), color, True, apply_grid_pattern, T, bbox)


class Roman(Prim):
    def __init__(self, T=None, color=None, apply_grid_pattern=False):

        bbox = AABB((-1, -1, -1), (1, 1, 1))

        super().__init__(RomanDAG(), color, True, apply_grid_pattern, T, bbox)

    def _gradient(self, x, y, z):
        a = 2.0 * x * y * y + 2.0 * x * z * z - 2.0 * y * z
        b = 2.0 * y * x * x + 2.0 * y * z * z - 2.0 * x * z
        c = 2.0 * z * x * x + 2.0 * z * y * y - 2.0 * x * y

        return (a, b, c)

    def normale(self, x, y, z):

        (a, b, c) = self._gradient(x, y, z)

        return normalize3((a, b, c))


class Steiner2(Prim):
    def __init__(self, T=None, color=None, apply_grid_pattern=False):

        super().__init__(Steiner2DAG(), color, True, apply_grid_pattern, T, None)


class Steiner4(Prim):
    def __init__(self, T=None, color=None, apply_grid_pattern=False):

        super().__init__(Steiner4DAG(), color, True, apply_grid_pattern, T, None)


class HyperboloidTwoSheets(Prim):
    def __init__(self, T=None, color=None, apply_grid_pattern=False):

        super().__init__(
            HyperboloidTwoSheetsDAG(), color, True, apply_grid_pattern, T, None
        )


class HyperboloidOneSheet(Prim):
    def __init__(self, T=None, color=None, apply_grid_pattern=False):

        super().__init__(
            HyperboloidOneSheetDAG(), color, True, apply_grid_pattern, T, None
        )


class HalfSpace(Prim):
    def __init__(self, color=None, T=None, apply_grid_pattern=False):
        # On peut réutiliser PlaneDAG car la normale est la même (surface plane)
        super().__init__(PlaneDAG(), color, True, apply_grid_pattern, T, None)

    def intersection(self, ray):
        trf_ray = ray
        if self.T is not None:
            trf_ray = ray.transform(~self.T)

        sz = trf_ray.origin[2]
        dz = trf_ray.direction[2]

        t_in = 0.0001
        t_out = 10000.0  # Fait office de "+infini" pour l'intervalle 1D

        # Résolution de l'intersection avec le plan z = 0
        t_root = -1.0
        if abs(dz) > 1e-6:
            t_root = -sz / dz

        # --- Logique de Volume ---
        if sz < 0:
            # On part de l'INTERIEUR du volume
            if dz > 1e-6:
                t_out = t_root  # On va vers le haut, on sort au point t_root
            # Si on va vers le bas (dz < 0), on reste dans la matière jusqu'à l'infini (t_out = 10000)
        else:
            # On part de l'EXTERIEUR du volume
            if dz < -1e-6:
                t_in = t_root  # On va vers le bas, on entre au point t_root
            else:
                return (
                    []
                )  # On monte ou on est parallèle, on ne touchera jamais la matière

        # Si l'intervalle est invalide ou derrière la caméra
        if t_in > t_out or t_out < 0.0001:
            return []

        # --- Création de l'intervalle volumique ---
        hit_a = self.compute_ray_hit(trf_ray, t_in)
        hit_b = self.compute_ray_hit(trf_ray, t_out)

        if self.T is not None:
            hit_a = self._local_to_world(hit_a, ray)
            hit_b = self._local_to_world(hit_b, ray)

        return [Intervalle(hit_a, hit_b)]

    def normale(self, x, y, z):
        # La normale pointe toujours vers l'extérieur du volume (vers les Z positifs)
        return normalize3((0.0, 0.0, 1.0))
