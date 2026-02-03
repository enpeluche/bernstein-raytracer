from PIL import Image
from Ray import Ray
from constants import *


class Scene:
    def __init__(self, camera, scene, background_color=(44, 55, 88)):

        self.camera = camera

        self.scene = scene

        self.background_color = background_color

        # il lui faut le contenu de la scene

    def raycasting(self):

        #

        pixels_buffer = []

        for zpix in range(self.camera.size_win, -self.camera.size_win - 1, -1):
            for xpix in range(-self.camera.size_win, self.camera.size_win + 1):

                rayon = self.camera.generate_ray(xpix, zpix)
                intervalles = self.scene.intersection(rayon)

                if [] == intervalles or intervalles == None:
                    (r, v, b) = self.background_color
                elif intervalles[0].a.t < FOG_START:
                    (r, v, b) = self.rendering(rayon, intervalles[0].a)
                elif intervalles[0].a.t > FOG_END:  # fog ?
                    (r, v, b) = self.background_color
                else:
                    dist = intervalles[0].a.t
                    fog_factor = (dist - FOG_START) / (FOG_END - FOG_START)
                    (r, v, b) = self.rendering(rayon, intervalles[0].a)
                    # Formule de mélange (Lerp) : (1-f)*Objet + f*Fond
                    bg_r, bg_v, bg_b = self.background_color

                    r = int(r * (1 - fog_factor) + bg_r * fog_factor)
                    v = int(v * (1 - fog_factor) + bg_v * fog_factor)
                    b = int(b * (1 - fog_factor) + bg_b * fog_factor)

                pixels_buffer.append((r, v, b))

        img = Image.new(
            "RGB", (2 * self.camera.size_win + 1, 2 * self.camera.size_win + 1)
        )
        img.putdata(pixels_buffer)

        return img

    def rendering(self, ray, rayHit):

        (rr, vv, bb) = rayHit.color
        (nx, ny, nz, d) = rayHit.plan
        (lx, ly, lz) = self.camera.light_dir

        oui = ray.direction[0] * nx + ray.direction[1] * ny + ray.direction[2] * nz

        if oui < 0:
            (rr, vv, bb) = (rr, vv, bb)
        else:
            (rr, vv, bb) = (255 - rr, 255 - vv, 255 - bb)

        ps = nx * lx + ny * ly + nz * lz

        # --- FIX 1 : Éclairage Double Face ---
        # On prend la valeur absolue. Que la normale soit à l'endroit ou à l'envers,
        # si la surface est face à la lumière, elle doit briller.
        diffuse_intensity = abs(ps)

        # --- FIX 2 : Point de départ de l'ombre (Shadow Bias) ---
        epsilon = 0.001

        # Si la normale pointe à l'opposé de la lumière (ps < 0),
        # il faut pousser le point dans l'AUTRE sens pour sortir de la surface.
        # Sinon, le rayon part DANS l'objet et croit qu'il est à l'ombre.
        bias_direction = 1.0 if ps > 0 else -1.0

        origin_shadow = (
            rayHit.pt[0] + nx * epsilon * bias_direction,
            rayHit.pt[1] + ny * epsilon * bias_direction,
            rayHit.pt[2] + nz * epsilon * bias_direction,
        )

        (nx, ny, nz, d) = rayHit.plan

        # 2. Recalcul de la direction du rayon (Vue)
        # Vecteur = Point Impact - Position Caméra
        vx = rayHit.pt[0] - self.camera.cam_o[0]
        vy = rayHit.pt[1] - self.camera.cam_o[1]
        vz = rayHit.pt[2] - self.camera.cam_o[2]

        import math

        dist_vue = math.sqrt(
            vx * vx + vy * vy + vz * vz
        )  # C'est théoriquement rayHit.t
        vx, vy, vz = vx / dist_vue, vy / dist_vue, vz / dist_vue

        spacing = 0.2  # Une ligne tous les 0.2 unités

        K = 0.002

        # Sécurité : alignement
        (nx, ny, nz, d) = rayHit.plan
        vx, vy, vz = (
            rayHit.pt[0] - self.camera.cam_o[0],
            rayHit.pt[1] - self.camera.cam_o[1],
            rayHit.pt[2] - self.camera.cam_o[2],
        )

        dist = math.sqrt(vx * vx + vy * vy + vz * vz)

        thickness = min(dist * K, spacing)

        # On décale un peu (+ spacing/2) pour éviter que la ligne tombe pile sur le défaut central (0,0,0)
        px = abs(rayHit.pt[0] + spacing / 2.0)
        py = abs(rayHit.pt[1] + spacing / 2.0)
        pz = abs(rayHit.pt[2] + spacing / 2.0)

        # Le reste de la division (ex: 0.05 ou 0.24)
        mx = px % spacing
        my = py % spacing
        mz = pz % spacing

        # Transformation en "Distance au bord le plus proche" (Onde triangulaire)
        # Ça permet d'avoir la ligne centrée sur le multiple
        dx = min(mx, spacing - mx)
        dy = min(my, spacing - my)
        dz = min(mz, spacing - mz)

        # 4. Dessin
        if dx < thickness or dy < thickness or dz < thickness:
            return (255, 255, 255)

        shadow_ray = Ray(origin_shadow, (lx, ly, lz))

        # Petite optimisation : on s'arrête au premier obstacle trouvé
        obstacles = self.scene.intersection(shadow_ray)
        is_in_shadow = False

        # Vérification rapide (si la liste n'est pas vide/None)
        if obstacles:
            is_in_shadow = True

        shadow_opacity = 0.86  # L'ombre n'est pas totalement noire
        ambient = 0.1

        # Application de l'intensité calculée plus haut
        diffuse = diffuse_intensity * 0.9

        if is_in_shadow:
            coef = ambient + diffuse * (1.0 - shadow_opacity)
        else:
            coef = ambient + diffuse

        coef = min(1.0, coef)

        return (int(coef * rr), int(coef * vv), int(coef * bb))

    def renderindg(self, rayHit):
        (rr, vv, bb) = rayHit.color
        (nx, ny, nz, d) = rayHit.plan
        (lx, ly, lz) = self.camera.light_dir

        ps = nx * lx + ny * ly + nz * lz

        if ps <= 0:
            ambient = 0.1

            return (
                int(ambient * rr),
                int(ambient * vv),
                int(ambient * bb),
            )

        epsilon = 0.001

        origin_shadow = (
            rayHit.pt[0] + nx * epsilon,
            rayHit.pt[1] + ny * epsilon,
            rayHit.pt[2] + nz * epsilon,
        )

        shadow_ray = Ray(origin_shadow, (lx, ly, lz))

        obstacles = self.scene.intersection(shadow_ray)

        is_in_shadow = False

        for intervalle in obstacles:
            is_in_shadow = True

        shadow_opacity = 0.86

        ambient = 0.1

        diffuse = max(0, ps * 0.9)

        if is_in_shadow:
            coef = ambient + diffuse * (1.0 - shadow_opacity)
        else:
            coef = ambient + diffuse

        coef = min(1.0, coef)
        return (int(coef * rr), int(coef * vv), int(coef * bb))
