from PIL import Image
from Ray import Ray
from constants import *
from math import sqrt

from Intervalle import *


class Scene:
    def __init__(self, camera, scene, background_color=(24, 140, 180)):

        self.camera = camera

        self.scene = scene

        self.background_color = background_color

        # il lui faut le contenu de la scene

    def raycasting(self):
        z_img = 0

        width = height = self.camera.size_win

        img = Image.new("RGB", (width, height))

        for zpix in range(height // 2, -height // 2, -1):

            row_pixels = []

            print(f"zpix: {zpix:05d}", end="\r")

            for xpix in range(-width // 2, width // 2):

                ray = self.camera.generate_ray(xpix, zpix)
                intervalles = self.scene.intersection(ray)

                if not intervalles:
                    row_pixels.append(self.background_color)
                    continue

                color = self.rendering(ray, intervalles[0].a)

                row_pixels.append(color)

            box = (0, z_img, width, z_img + 1)

            line_img = Image.new("RGB", (width, 1))
            line_img.putdata(row_pixels)
            img.paste(line_img, box)

            z_img += 1

        return img

    def rendering(self, ray, rayHit):

        (red, green, blue) = rayHit.color

        (red, green, blue) = self._apply_face_color(ray, rayHit)

        (red, green, blue) = self._apply_lighting(
            rayHit.pt, rayHit.plan, (red, green, blue)
        )

        # (red, green, blue) = self._apply_grid_pattern(rayHit, (red, green, blue))

        (red, green, blue) = self._apply_fog(rayHit.t, (red, green, blue))

        return (red, green, blue)

    def _apply_fog(self, t, color):
        if t < FOG_START:
            return color

        if t > FOG_END:
            return self.background_color

        bg_r, bg_g, bg_b = self.background_color
        red, green, blue = color

        fog = (t - FOG_START) / (FOG_END - FOG_START)

        inv_fog = 1 - fog

        red = int(red * inv_fog + bg_r * fog)
        green = int(green * inv_fog + bg_g * fog)
        blue = int(blue * inv_fog + bg_b * fog)

        return (red, green, blue)

    def _apply_face_color(self, ray, rayHit):
        # je suis certain que cela fait ce que ça fait ?
        (nx, ny, nz, d) = rayHit.plan

        dot_product = (
            ray.direction[0] * nx + ray.direction[1] * ny + ray.direction[2] * nz
        )

        if dot_product < 0:
            return rayHit.color

        (r, g, b) = rayHit.color

        return (255 - r, 255 - g, 255 - b)

    def _apply_lighting(self, pt, plan, color):
        (rr, vv, bb) = color
        (nx, ny, nz, d) = plan
        (lx, ly, lz) = self.camera.light_dir

        # sert à calculer l'angle entre lalumière et la normale
        ps = nx * lx + ny * ly + nz * lz

        # utile ? à voir
        diffuse_intensity = abs(ps)
        diffuse = diffuse_intensity * 0.9

        bias_direction = 1.0 if ps > 0 else -1.0

        origin_shadow = (
            pt[0] + nx * shadow_bias * bias_direction,
            pt[1] + ny * shadow_bias * bias_direction,
            pt[2] + nz * shadow_bias * bias_direction,
        )

        shadow_ray = Ray(origin_shadow, (lx, ly, lz))

        obstacles = self.scene.intersection(shadow_ray)

        if obstacles:
            coef = ambient + diffuse * (1.0 - shadow_opacity)
        else:
            coef = ambient + diffuse

        coef = min(1.0, coef)

        return (int(coef * rr), int(coef * vv), int(coef * bb))

    def _apply_grid_pattern(self, rayHit, color):
        vx = rayHit.pt[0] - self.camera.cam_o[0]
        vy = rayHit.pt[1] - self.camera.cam_o[1]
        vz = rayHit.pt[2] - self.camera.cam_o[2]

        dist = sqrt(vx * vx + vy * vy + vz * vz)

        if dist < 0.0001:
            return color

        vx, vy, vz = vx / dist, vy / dist, vz / dist

        spacing = 0.25

        K = 0.0008

        base_thickness = 0.003

        max_allowed_thickness = spacing * 0.4

        raw_thickness = base_thickness + (dist * K)
        thickness = min(raw_thickness, max_allowed_thickness)

        px = abs(rayHit.pt[0] + spacing / 2.0)
        py = abs(rayHit.pt[1] + spacing / 2.0)
        pz = abs(rayHit.pt[2] + spacing / 2.0)

        mx = px % spacing
        my = py % spacing
        mz = pz % spacing

        dx = min(mx, spacing - mx)
        dy = min(my, spacing - my)
        dz = min(mz, spacing - mz)

        if dx < thickness or dy < thickness or dz < thickness:

            fade_factor = 1.0
            if dist > 5.0:

                fade_factor = max(0.3, 1.0 - (dist - 10.0) * 0.05)

            grid_r, grid_g, grid_b = 255 - color[0], 255 - color[1], 255 - color[2]
            obj_r, obj_g, obj_b = color

            final_r = int(obj_r * (1 - fade_factor) + grid_r * fade_factor)
            final_g = int(obj_g * (1 - fade_factor) + grid_g * fade_factor)
            final_b = int(obj_b * (1 - fade_factor) + grid_b * fade_factor)

            return (final_r, final_g, final_b)
        else:
            return color
