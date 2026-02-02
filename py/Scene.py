from PIL import Image, ImageDraw, ImageFont
from util import clamp
import time
import random
from Ray import Ray
import os
import shutil


class Scene:
    def __init__(self, camera, scene, background_color=(44, 55, 88)):

        self.camera = camera

        self.scene = scene

        self.background_color = background_color

        # il lui faut le contenu de la scene

    def raycasting(self):
        start = time.perf_counter()

        print("Début de génération de l'image.")

        pixels_buffer = []

        for zpix in range(self.camera.size_win, -self.camera.size_win - 1, -1):
            for xpix in range(-self.camera.size_win, self.camera.size_win + 1):
                rayon = self.camera.generate_ray(xpix, zpix)
                intervalles = self.scene.intersection(rayon)

                if [] == intervalles or intervalles == None:
                    (r, v, b) = self.background_color
                # elif intervalles[0].a.t > 10: # fog ?
                #    (r, v, b) = self.background_color
                else:
                    (r, v, b) = self.rendering(intervalles[0].a)

                pixels_buffer.append((r, v, b))

        img = Image.new(
            "RGB", (2 * self.camera.size_win + 1, 2 * self.camera.size_win + 1)
        )
        img.putdata(pixels_buffer)
        end = time.perf_counter()
        print(f"Temps d'exécution : {end - start:.6f} secondes")
        return img

    def rendering(self, rayHit):
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
        epsilon = 1e-3
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

        shadow_opacity = 0.96

        ambient = 0.1

        diffuse = max(0, ps) * 0.9

        if is_in_shadow:
            coef = ambient + diffuse * (1.0 - shadow_opacity)
        else:
            coef = ambient + diffuse

        coef = min(1.0, coef)
        return (int(coef * rr), int(coef * vv), int(coef * bb))
