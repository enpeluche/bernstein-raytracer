from DAG import *
from solveracine import *
from util import *
from bool1d import *
from Matrix import *
from AABB import AABB

from Intervalle import Intervalle
from RayHit import RayHit

from Transformation import *


class Obj:
    def __init__(self):
        " "


class Prim(Obj):
    def __init__(self, fonc_xyz, color, T=None, bbox=None):
        self.fonc = fonc_xyz
        self.color = color

        if T is None:
            T = identity()

        self.T = T

        if bbox is None:
            inf = float("inf")
            self.bbox = AABB((-inf, -inf, -inf), (inf, inf, inf))
        else:
            self.bbox = bbox

    def __add__(self, B):
        return Union(self, B)

    def __and__(self, B):
        return Inter(self, B)

    def __sub__(self, B):
        return Differ(self, B)

    def transform(self, T):
        self.T = T * self.T
        return self

    def translate(self, tx, ty, tz):
        self.transform(translation(tx, ty, tz))
        return self

    def rotate_x(self, θ):
        self.transform(rotation_x(θ))
        return self

    def rotate_y(self, θ):
        self.transform(rotation_y(θ))
        return self

    def rotate_z(self, θ):
        self.transform(rotation_z(θ))
        return self

    def scale(self, a, b, c):
        self.transform(scaling(a, b, c))
        return self

    def compute_ray_hit(self, ray, t):  # t est une racine | create ray hit plutôt ?
        (sx, sy, sz) = ray.origin
        (dx, dy, dz) = ray.direction

        x = sx + dx * t
        y = sy + dy * t
        z = sz + dz * t
        pt = (x, y, z)

        (a, b, c) = self.normale(x, y, z)

        d = a * x + b * y + c * z

        plan = (a, b, c, d)

        return RayHit(t, pt, plan, self.color)

    def intersection(self, ray):

        trf_ray = ray
        if self.T != None:
            trf_ray = ray.transform(~self.T)

        if not self.bbox.intersection(trf_ray):
            return []

        poly_x = Polynome([trf_ray.origin[0], trf_ray.direction[0]])
        poly_y = Polynome([trf_ray.origin[1], trf_ray.direction[1]])
        poly_z = Polynome([trf_ray.origin[2], trf_ray.direction[2]])

        pol_t = self.fonc.to_poly({"x": poly_x, "y": poly_y, "z": poly_z})

        roots = racine(pol_t.vect())

        intervalles = []

        if roots:
            for i in range(0, len(roots) - 1, 2):

                t_in = roots[i]
                t_out = roots[i + 1]

                if t_out < 0.0001:
                    continue

                if t_in < 0.0001:
                    t_in = 0.0001

                hit_a = self.compute_ray_hit(trf_ray, roots[i])
                hit_b = self.compute_ray_hit(trf_ray, roots[i + 1])

                if self.T is not None:
                    hit_a = self._local_to_world(hit_a, ray)
                    hit_b = self._local_to_world(hit_b, ray)

                intervalles.append(Intervalle(hit_a, hit_b))

        return intervalles

    def _local_to_world(self, hit, ray_world):
        m_fwd = self.T.forward.mat
        m_bwd = self.T.backward.mat

        lx, ly, lz = hit.pt
        px = m_fwd[0][0] * lx + m_fwd[0][1] * ly + m_fwd[0][2] * lz + m_fwd[0][3]
        py = m_fwd[1][0] * lx + m_fwd[1][1] * ly + m_fwd[1][2] * lz + m_fwd[1][3]
        pz = m_fwd[2][0] * lx + m_fwd[2][1] * ly + m_fwd[2][2] * lz + m_fwd[2][3]

        hit.pt = (px, py, pz)

        lnx, lny, lnz = hit.plan[0], hit.plan[1], hit.plan[2]

        nx = m_bwd[0][0] * lnx + m_bwd[1][0] * lny + m_bwd[2][0] * lnz
        ny = m_bwd[0][1] * lnx + m_bwd[1][1] * lny + m_bwd[2][1] * lnz
        nz = m_bwd[0][2] * lnx + m_bwd[1][2] * lny + m_bwd[2][2] * lnz

        length_sq = nx * nx + ny * ny + nz * nz
        if length_sq > 0:
            inv_len = 1.0 / (length_sq ** 0.5)
            nx *= inv_len
            ny *= inv_len
            nz *= inv_len

        d = -(nx * px + ny * py + nz * pz)
        hit.plan = (nx, ny, nz, d)

        vx = px - ray_world.origin[0]
        vy = py - ray_world.origin[1]
        vz = pz - ray_world.origin[2]

        rdx, rdy, rdz = ray_world.direction
        hit.t = vx * rdx + vy * rdy + vz * rdz

        return hit

    def _local_toto_world(self, hit, ray_world):

        pt_mat = Matrix([[hit.pt[0]], [hit.pt[1]], [hit.pt[2]], [1]])
        res_pt = self.T.forward * pt_mat

        px, py, pz = res_pt[0, 0], res_pt[1, 0], res_pt[2, 0]
        hit.pt = (px, py, pz)

        old_nx, old_ny, old_nz = hit.plan[0], hit.plan[1], hit.plan[2]

        norm_mat = Matrix([[old_nx], [old_ny], [old_nz], [0]])

        mat_normale = self.T.backward.transpose()
        res_norm = mat_normale * norm_mat

        nx, ny, nz = res_norm[0, 0], res_norm[1, 0], res_norm[2, 0]
        length = (nx * nx + ny * ny + nz * nz) ** 0.5

        if length > 0:
            nx, ny, nz = nx / length, ny / length, nz / length

        d = -(nx * px + ny * py + nz * pz)

        hit.plan = (nx, ny, nz, d)

        dx = px - ray_world.origin[0]
        dy = py - ray_world.origin[1]
        dz = pz - ray_world.origin[2]
        vx = hit.pt[0] - ray_world.origin[0]
        vy = hit.pt[1] - ray_world.origin[1]
        vz = hit.pt[2] - ray_world.origin[2]

        dx, dy, dz = ray_world.direction
        hit.t = vx * dx + vy * dy + vz * dz

        return hit

    def normale(self, x, y, z):
        fx = self.fonc.derivee("x")
        fy = self.fonc.derivee("y")
        fz = self.fonc.derivee("z")
        dico = {"x": x, "y": y, "z": z}
        (a, b, c) = (fx.eval(dico), fy.eval(dico), fz.eval(dico))
        return normalize3((a, b, c))

        # dico = {
        #    "x": Nb(rayon.source[0]) + Nb(rayon.dir[0]) * Var("t"),
        #    "y": Nb(rayon.source[1]) + Nb(rayon.dir[1]) * Var("t"),
        #    "z": Nb(rayon.source[2]) + Nb(rayon.dir[2]) * Var("t"),
        # }
        # expression_en_t = self.fonc.evalsymb(dico)

        # pol_t = expression_en_t.topolent()


class Union(Prim):
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def intersection(self, ray):

        return union(self.a.intersection(ray), self.b.intersection(ray))


class Inter(Prim):
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def intersection(self, ray):
        return inter(self.a.intersection(ray), self.b.intersection(ray))

    def transform(self, T):
        self.a.T = T * self.a.T
        self.b.T = T * self.b.T

        return self

    def translate(self, tx, ty, tz):
        T = translation(tx, ty, tz)
        self.a.T = T * self.a.T
        self.b.T = T * self.b.T
        return self

    def rotate_x(self, θ):
        T = rotation_x(θ)
        self.a.T = T * self.a.T
        self.b.T = T * self.b.T
        return self

    def rotate_y(self, θ):
        T = rotation_y(θ)
        self.a.T = T * self.a.T
        self.b.T = T * self.b.T
        return self

    def rotate_z(self, θ):
        T = rotation_z(θ)
        self.a.T = T * self.a.T
        self.b.T = T * self.b.T
        return self

    def scale(self, a, b, c):
        T = scaling(a, b, c)
        self.a.T = T * self.a.T
        self.b.T = T * self.b.T
        return self


class Differ(Prim):
    def __init__(self, a, b):
        self.T = identity()

        self.a = a
        self.b = b

    def transform(self, T):
        self.a.T = T * self.a.T
        self.b.T = T * self.b.T

        return self

    def translate(self, tx, ty, tz):
        T = translation(tx, ty, tz)
        self.a.T = T * self.a.T
        self.b.T = T * self.b.T
        return self

    def rotate_x(self, θ):
        T = rotation_x(θ)
        self.a.T = T * self.a.T
        self.b.T = T * self.b.T
        return self

    def rotate_y(self, θ):
        T = rotation_y(θ)
        self.a.T = T * self.a.T
        self.b.T = T * self.b.T
        return self

    def rotate_z(self, θ):
        T = rotation_z(θ)
        self.a.T = T * self.a.T
        self.b.T = T * self.b.T
        return self

    def scale(self, a, b, c):
        T = scaling(a, b, c)
        self.a.T = T * self.a.T
        self.b.T = T * self.b.T
        return self

    def intersection(self, ray):
        return differ(self.a.intersection(ray), self.b.intersection(ray))
