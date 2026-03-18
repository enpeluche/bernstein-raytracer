from .base import GeometryObject

from ..constants import (
    GRID_SPACING,
    GRID_THICKNESS_SCALE,
    GRID_BASE_THICKNESS,
    GRID_MAX_THICKNESS,
)

from ..util import normalize3, dot3
from ..RayHit import RayHit
from ..DAG.compiler import (
    optimize_patterns,
    compile_dag_evaluator,
    analyze_primitive_compiler,
)
from ..transformation import *
from ..Interval import Interval
from ..constants import EPSILON as ε, RAY_PROTOCOL, NORMAL_PROTOCOL


# TODO : # limite pareil un cache ou mémoire partagée ici, slot
inf = float("inf")
from ..Polynomial import *
from ..DAG.variable import Variable

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
        debug=False,
    ):
        from .AABB import AABB
        from ..util import random_color

        if debug:
            analyze_primitive_compiler(implicit_function, label, env)

        Pf = implicit_function.to_polynomial(env)
        Pf_opt = [optimize_patterns(c) for c in Pf.coefficients]
        self.f_evaluator, _ = compile_dag_evaluator(Pf_opt, forced_args=RAY_PROTOCOL)

        dfx = implicit_function.partial_derivative("x")
        dfy = implicit_function.partial_derivative("y")
        dfz = implicit_function.partial_derivative("z")

        df_nodes = [
            optimize_patterns(dfx),
            optimize_patterns(dfy),
            optimize_patterns(dfz),
        ]
        #
        self.df_evaluator, _ = compile_dag_evaluator(
            df_nodes, forced_args=NORMAL_PROTOCOL
        )

        self.dual_color = dual_color
        self.show_grid = show_grid

        self.label = label

        self.color = color if color is not None else random_color()

        self.transformation = identity() if transformation is None else transformation

        self.aabb = AABB((-inf, -inf, -inf), (inf, inf, inf)) if aabb is None else aabb

    def transform(self, transformation: Transformation) -> "Primitive":
        self.transformation = transformation * self.transformation

        return self

    def evaluate_hit(self, local_ray, t: float, debug: bool = False) -> RayHit:
        """Compute geometric intersection details for a ray-surface hit.

        Calculates the 3D impact point using the ray parameter t, evaluates the
        surface normal at that location, and determines the face orientation
        (front or back) to properly align the normal for lighting calculations.

        Args:
            local_ray (Ray): The ray instance that intersected the surface.
            t (float): The distance along the ray where the hit occurred.

        Returns:
            RayHit: A container holding the primitive reference, the hit distance,
            the 3D impact point, the correctly oriented normal, and the face flag.
        """
        ox, oy, oz = local_ray.origin
        dx, dy, dz = local_ray.direction

        # 1. Point d'impact dans le repère local.
        local_impact_point = (
            ox + dx * t,
            oy + dy * t,
            oz + dz * t,
        )

        # 2. Normale dans le repère local.

        local_normal = self.normal_at(local_impact_point)

        # 3. Orientation de la face (repère local).

        EPS_ORIENT = 1e-7

        dot_product = dot3(local_ray.direction, local_normal)

        if dot_product < -EPS_ORIENT:
            is_front_face = True
        elif dot_product > EPS_ORIENT:
            is_front_face = False
        else:
            # zone instable → décider de façon cohérente
            is_front_face = True

        if not is_front_face:
            local_normal = (
                -local_normal[0],
                -local_normal[1],
                -local_normal[2],
            )

        if self.transformation is None:
            world_impact_point = local_impact_point
            world_normal = local_normal

        else:
            m_fwd = self.transformation.forward.mat
            m_bwd = self.transformation.backward.mat

            # 3. Point d'impact dans le repère parent.
            world_impact_point = Primitive._local_to_world_point(
                local_impact_point, m_fwd
            )

            # 4. Normale dans le repère parent.
            world_normal = Primitive._local_to_world_normal(local_normal, m_bwd)

        hit = RayHit(
            self,
            t,
            local_impact_point,
            world_impact_point,
            local_normal,
            world_normal,
            is_front_face,
        )

        if debug:
            print(hit)
        return hit

    def any_intersection(self, ray) -> bool:
        """
        Détermine si il y a au moins une intersection.
        """

        # Early-exit optimization: Since the AABB and the ray are both in world space,
        # we perform a world-space intersection test first. If the ray misses the
        # bounding box, we avoid the computational overhead.
        if not self.aabb.intersection(ray):
            return False

        # Map the world-space ray into the object's local (canonical) space
        # using the inverse transformation.
        local_ray = (
            ray.transform(~self.transformation)
            if self.transformation is not None
            else ray
        )

        numeric_coeffs = self.f_evaluator(*local_ray.eval_params)

        return Polynomial(numeric_coeffs).has_any_root(local_ray.t_min, local_ray.t_max)

    def intersection(self, ray, debug=False):
        """Trouve les intervalles d'intersection entre un rayon et la surface."""

        if debug:
            print(f"    World {ray}")

        # Early-exit optimization: Since the AABB and the ray are both in world space,
        # we perform a world-space intersection test first. If the ray misses the
        # bounding box, we avoid the computational overhead.
        is_aabb_hit = self.aabb.intersection(ray)

        if debug:
            print(f"    AABB Hit  : {is_aabb_hit}")

        if not is_aabb_hit:
            return []

        # Map the world-space ray into the object's local (canonical) space
        # using the inverse transformation.
        local_ray = (
            ray.transform(~self.transformation)
            if self.transformation is not None
            else ray
        )

        if debug:
            print(f"    Local {local_ray}")

        numeric_coeffs = self.f_evaluator(*local_ray.eval_params)

        if debug:
            # On formate uniquement pour le confort visuel (5 chiffres après la virgule)
            coeffs_lisibles = [f"{c:.5f}" for c in numeric_coeffs]
            print(f"coefficients of polynomial : {coeffs_lisibles}")

        POL = Polynomial(numeric_coeffs)

        # Extract real roots via Bernstein basis subdivision. The de Casteljau-based
        # algorithm inherently produces roots in ascending order.
        roots = POL.roots(local_ray.t_min, local_ray.t_max)

        if debug:
            print(f"roots : {roots}")

        roots = [r for r in roots if local_ray.t_min + EPSILON < r < local_ray.t_max]

        if debug:
            import matplotlib.pyplot as plt

            # On crée 200 points entre t=0 et t=max(roots) + 1 (pour voir un peu après)
            t_fin = max(roots) + 1.0 if roots else 10.0
            t_vals = [t_fin * i / 200.0 for i in range(201)]
            y_vals = [POL(t) for t in t_vals]

            plt.figure(figsize=(8, 4))
            plt.title("Profil de l'intersection P(t)")

            # La courbe du polynôme
            plt.plot(t_vals, y_vals, label="P(t)", color="blue")

            # La ligne zéro (le rayon de lumière)
            plt.axhline(0, color="red", linestyle="--", label="Rayon (Zéro)")

            # On place des gros points verts sur les racines trouvées
            for r in roots:
                plt.scatter([r], [0], color="green", zorder=5, s=80)
                plt.annotate(
                    f"t={r:.3f}",
                    (r, 0),
                    textcoords="offset points",
                    xytext=(0, 10),
                    ha="center",
                )

            # ... (tout le code de configuration du plot reste identique) ...
            plt.legend()
            plt.grid(True)

            # 1. On sauvegarde l'image dans le dossier partagé
            plt.savefig("debug_pixel_graph.png")

            # 2. On ferme la figure pour libérer la mémoire
            plt.close()

        # "I've got no roots..." — Alice Merton.
        # Early exit: the ray misses the surface geometry entirely.
        if not roots:
            return []

        intervals = []

        if len(roots) == 1:
            root = roots[0]
            if root > ray.t_max:
                return []

            if root < ray.t_min:
                root = ray.t_min

            hit = self.evaluate_hit(local_ray, root, debug=debug)
            return [Interval(hit, hit)]

        if len(POL.coefficients) == 3:  # degré 2

            if len(roots) == 2:  # 2 racines
                impact_time_in = roots[0]
                impact_time_out = roots[1]

                hit_a = self.evaluate_hit(local_ray, impact_time_in, debug=debug)
                hit_b = self.evaluate_hit(local_ray, impact_time_out, debug=debug)

                intervals.append(Interval(hit_a, hit_b))

                return intervals

        eps = 1e-6
        events = []

        # 1. Qualification des racines (L'approche Epsilon)
        for root in roots:
            # On regarde les valeurs justes avant et juste après
            val_before = POL(root - eps)
            val_after = POL(root + eps)

            # On classifie selon le changement de signe
            if val_before > 0 and val_after <= 0:
                events.append(("IN", root))
            elif val_before < 0 and val_after >= 0:
                events.append(("OUT", root))
            else:
                # Aucun changement de signe = Tangence ou Singularité (le "manche" de Whitney)
                events.append(("TOUCH", root))

        intervals = []

        # Création des intervalles par paires (Entrée -> Sortie)
        for i in range(0, len(roots) - 1):
            impact_time_in = roots[i]
            # on doit regarder les signes de POL(roots[i] - epsilon) et POL(roots[i] + epsilon)
            # on doit regarder les signes de POL(roots[i+1] - epsilon) et POL(roots[i+1] + epsilon)
            # si ya pas de changement de signe : tangante donc on oubli la racine ?
            impact_time_out = roots[i + 1]

            mid_t = (impact_time_in + impact_time_out) * 0.5

            if POL(mid_t) < 0:

                # ici on regarde le point au rayon
                if impact_time_out < ray.t_min:  # culling
                    continue

                if impact_time_in > ray.t_max:
                    break

                if impact_time_in < ray.t_min:
                    impact_time_in = ray.t_min

                #  ici avec cette méthode le repère parent est le monde
                hit_a = self.evaluate_hit(local_ray, impact_time_in, debug=debug)
                hit_b = self.evaluate_hit(local_ray, impact_time_out, debug=debug)

                intervals.append(Interval(hit_a, hit_b))

        return intervals

    @staticmethod
    def _local_to_world_point(local_impact_point, m_fwd):

        lx, ly, lz = local_impact_point
        px = m_fwd[0][0] * lx + m_fwd[0][1] * ly + m_fwd[0][2] * lz + m_fwd[0][3]
        py = m_fwd[1][0] * lx + m_fwd[1][1] * ly + m_fwd[1][2] * lz + m_fwd[1][3]
        pz = m_fwd[2][0] * lx + m_fwd[2][1] * ly + m_fwd[2][2] * lz + m_fwd[2][3]

        return (px, py, pz)

    @staticmethod
    def _local_to_world_normal(local_normal, m_bwd):
        # 2. transform_normal -> en faire _transform_normal
        lnx, lny, lnz = local_normal

        nx = m_bwd[0][0] * lnx + m_bwd[1][0] * lny + m_bwd[2][0] * lnz
        ny = m_bwd[0][1] * lnx + m_bwd[1][1] * lny + m_bwd[2][1] * lnz
        nz = m_bwd[0][2] * lnx + m_bwd[1][2] * lny + m_bwd[2][2] * lnz

        length_sq = nx * nx + ny * ny + nz * nz
        if length_sq > 0:
            inv_len = 1.0 / (length_sq ** 0.5)
            nx *= inv_len
            ny *= inv_len
            nz *= inv_len

        return (nx, ny, nz)

    def normal_at(self, point):
        x, y, z = point

        nx, ny, nz = self.df_evaluator(x, y, z)
        return normalize3((nx, ny, nz))
        # norm2 = nx * nx + ny * ny + nz * nz

        if norm2 < 1e-10:
            eps = 1e-5

            fx1 = self.f_evaluator(x + eps, y, z)
            fx2 = self.f_evaluator(x - eps, y, z)
            fy1 = self.f_evaluator(x, y + eps, z)
            fy2 = self.f_evaluator(x, y - eps, z)
            fz1 = self.f_evaluator(x, y, z + eps)
            fz2 = self.f_evaluator(x, y, z - eps)

            nx = fx1 - fx2
            ny = fy1 - fy2
            nz = fz1 - fz2

            norm2 = nx * nx + ny * ny + nz * nz

            if norm2 < 1e-12:
                return None  # mieux que (0,1,0)

        return normalize3((nx, ny, nz))

    def get_surface_color(self, rayHit, debug=False):
        """Pipeline de surface : calcule la teinte finale de l'objet (Local)."""

        # 1. On part de la couleur de base (avec gestion Dual Color)
        if self.dual_color:
            current_color = self._dual_color(rayHit)
        else:
            current_color = self.color

        # 2. On applique la grille par-dessus (si activée)
        if self.show_grid:
            current_color = self._compute_grid_shading(rayHit, current_color)

        return current_color

    def _dual_color(self, rayHit):  # à voir si je peux pas la rendre static
        """Retourne la couleur de l'objet ou son inverse si on tape l'intérieur."""

        if rayHit.is_front_face:
            return self.color

        # Si on est à l'intérieur, on inverse la couleur
        (r, g, b) = self.color
        return (255 - r, 255 - g, 255 - b)

    def _compute_grid_shading(
        self, rayHit, current_color
    ):  # à voir si je peux pas la rendre static
        dist = rayHit.impact_time

        if dist < 0.0001:
            return current_color

        raw_thickness = GRID_BASE_THICKNESS + (dist * GRID_THICKNESS_SCALE)
        thickness = min(raw_thickness, GRID_MAX_THICKNESS)

        px = abs(rayHit.local_impact_point[0] + GRID_SPACING / 2.0)
        pz = abs(rayHit.local_impact_point[2] + GRID_SPACING / 2.0)

        mx = px % GRID_SPACING
        mz = pz % GRID_SPACING

        dx = min(mx, GRID_SPACING - mx)
        dz = min(mz, GRID_SPACING - mz)

        if dx < thickness or dz < thickness:

            fade_factor = 1.0
            if dist > 5.0:

                fade_factor = max(
                    0.3, 1.0 - (dist - 10.0) * 0.05
                )  # soucis ici:fade_factor = max(0.3, min(1.0, 1.0 - (dist - 5.0) * 0.05))

            grid_r, grid_g, grid_b = (
                255 - current_color[0],
                255 - current_color[1],
                255 - current_color[2],
            )
            obj_r, obj_g, obj_b = current_color

            final_r = int(obj_r * (1 - fade_factor) + grid_r * fade_factor)
            final_g = int(obj_g * (1 - fade_factor) + grid_g * fade_factor)
            final_b = int(obj_b * (1 - fade_factor) + grid_b * fade_factor)

            return (final_r, final_g, final_b)
        else:
            return current_color
