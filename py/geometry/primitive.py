from .base import GeometryObject
from .AABB import AABB
from util import normalize3, dot3, random_color
from RayHit import RayHit
from DAG.compiler import (
    optimize_patterns,
    generate_python_poly_function,
    analyze_primitive_compiler,
)
from transformation import *
from Interval import Interval
from constants import EPSILON as ε

# TODO : # limite pareil un cache ou mémoire partagée ici, slot
inf = float("inf")
from Polynomial import *
from DAG import *

ox, oy, oz = Variable.make("ox"), Variable.make("oy"), Variable.make("oz")
dx, dy, dz = Variable.make("dx"), Variable.make("dy"), Variable.make("dz")

env = {
    "x": Polynomial([ox, dx]),
    "y": Polynomial([oy, dy]),
    "z": Polynomial([oz, dz]),
}


class Primitive(GeometryObject):
    """
    Représente une primitive géométrique définie par une fonction implicite (DAG).
    C'est la feuille de l'arbre CSG qui effectue les vrais calculs d'intersection.
    """

    __slots__ = (
        "f_evaluator",
        "df_evaluator",
        "dual_color",
        "show_grid",
        "label",
        "color",
        "transformation",
    )

    def __init__(
        self,
        implicit_function,
        color,
        dual_color=True,
        show_grid=False,
        transformation=None,
        aabb=None,
        label="unknown",
    ):

        analyze_primitive_compiler(implicit_function, label, env)
        Pf = implicit_function.to_polynomial(env)
        Pf_opt = [optimize_patterns(c) for c in Pf.coefficients]
        self.f_evaluator, _ = generate_python_poly_function(Pf_opt, False)

        dfx = implicit_function.partial_derivative("x")
        dfy = implicit_function.partial_derivative("y")
        dfz = implicit_function.partial_derivative("z")

        df_nodes = [
            optimize_patterns(dfx),
            optimize_patterns(dfy),
            optimize_patterns(dfz),
        ]
        #
        self.df_evaluator, _ = generate_python_poly_function(df_nodes, True)

        self.dual_color = dual_color
        self.show_grid = show_grid

        self.label = label

        self.color = color if color is not None else random_color()

        self.transformation = identity() if transformation is None else transformation

        self.aabb = AABB((-inf, -inf, -inf), (inf, inf, inf)) if aabb is None else aabb

    def transform(self, transformation: Transformation) -> "Primitive":
        self.transformation = transformation * self.transformation

        return self

    def evaluate_hit(self, ray, t: float) -> RayHit:
        """Compute geometric intersection details for a ray-surface hit.

        Calculate the 3D impact point using the ray parameter t, evaluate the
        surface normal at that location, and derive the homogeneous plane
        equation (ax + by + cz = d). Aggregate these geometric properties with
        the primitive's visual attributes into a RayHit container.

        Args:
            ray (Ray): The ray instance that intersected the surface.
            t (float): The distance along the ray where the hit occurred.

        Returns:
            RayHit: A container holding the hit distance, the 3D impact point,
                the plane equation (normal and d), the primitive color, and
                rendering flags for face color and grid patterns.
        """

        ox, oy, oz = ray.origin
        dx, dy, dz = ray.direction

        impact_point = (ox + dx * t, oy + dy * t, oz + dz * t)

        normal = self.normal_at(impact_point)

        d = dot3(impact_point, normal)

        plan = (*normal, d)

        return RayHit(
            t,
            impact_point,
            plan,
            self.color,
            self.dual_color,
            self.show_grid,
        )

    def intersection(self, ray):
        """Trouve les intervalles d'intersection entre un rayon et la surface."""

        # on test l'intersection avec le rayon non transformé
        if not self.aabb.intersection(ray):
            return []

        trf_ray = ray

        if self.transformation is not None:
            trf_ray = ray.transform(~self.transformation)

        eval_env = trf_ray.get_env()

        numeric_coeffs = self.f_evaluator(**eval_env)

        pol_t = Polynomial(numeric_coeffs)

        roots = pol_t.roots()

        if not roots:
            return []

        intervals = []

        if len(roots) == 1:  # vraiment ?
            # print("Une racine tangente !")
            roots = [roots[0], roots[0]]

        # Création des intervalles par paires (Entrée -> Sortie)
        for i in range(0, len(roots) - 1, 2):
            t_in = roots[i]
            t_out = roots[i + 1]

            if t_out < 0.0001:
                continue

            if t_in < 0.01:
                t_in = 0.01

            if t_in > 10:
                continue

            hit_a = self.evaluate_hit(trf_ray, roots[i])
            hit_b = self.evaluate_hit(trf_ray, roots[i + 1])

            if self.transformation is not None:
                hit_a = self._local_to_world(hit_a, ray)
                hit_b = self._local_to_world(hit_b, ray)

            intervals.append(Interval(hit_a, hit_b))

        return intervals

    def _local_to_world(self, hit, ray_world):
        """Ramène un point d'impact de l'espace local vers l'espace monde."""
        m_fwd = self.transformation.forward.mat
        m_bwd = self.transformation.backward.mat

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

    def normal_at(self, point):
        x, y, z = point
        nx, ny, nz = self.df_evaluator(x, y, z)

        # faire un fallback ici

        return normalize3((nx, ny, nz))

    def normal_at(self, point):
        """Evaluate the surface normal using df_evaluator with a jittered fallback."""
        x, y, z = point
        try:
            # 1. Tentative analytique directe
            nx, ny, nz = self.df_evaluator(x, y, z)

            # On vérifie la norme au carré contre ε² pour la cohérence dimensionnelle
            norm_sq = nx * nx + ny * ny + nz * nz
            if norm_sq < 1e-10:  #
                raise ValueError("Vanishing gradient")

        except Exception:
            # 2. FALLBACK : On décale le point d'évaluation pour sortir de la singularité
            # self.fallback_count += 1
            # print(f"⚠️ [Fallback] Normal jittered ({self.fallback_count} times)")

            # On évalue la dérivée analytique juste à côté (décalage de ε sur les 3 axes)
            # C'est beaucoup plus rapide que 6 appels de différence centrale !
            nx, ny, nz = self.df_evaluator(x + ε, y + ε, z + ε)

        return normalize3((nx, ny, nz))
