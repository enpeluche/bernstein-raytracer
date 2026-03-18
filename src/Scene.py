from PIL import Image
from .Ray import Ray
from .constants import *


class Scene:
    def __init__(self, camera, scene, background_color=(24, 140, 180)):

        self.camera = camera

        self.scene = scene

        self.background_color = background_color

    def raycasting(self, debug_pixels=None):
        z_img = 0

        width = height = self.camera.size_win

        img = Image.new("RGB", (width, height))

        for zpix in range(height):

            row_pixels = []

            for xpix in range(width):
                # fmt: off
                is_debug = ((xpix, zpix) in debug_pixels)

                if is_debug:
                    print(f"======DEBUG DU PIXEL ({xpix},{zpix})======\n")
                # fmt: on
                ray = self.camera.generate_ray(xpix, zpix)

                if ray is None:
                    row_pixels.append(self.background_color)
                    continue

                intervals = self.scene.intersection(ray, debug=is_debug)
                if is_debug:
                    print(
                        f"Couleur calculée: {self.rendering(intervals[0].hit_in, debug=is_debug)}"
                    )

                if is_debug:
                    row_pixels.append(RED)
                    continue
                if not intervals:
                    row_pixels.append(self.background_color)
                    continue

                color = (
                    RED
                    if is_debug
                    else self.rendering(intervals[0].hit_in, debug=is_debug)
                )  # on rend le premier trouvé

                row_pixels.append(color)

            box = (0, z_img, width, z_img + 1)

            line_img = Image.new("RGB", (width, 1))
            line_img.putdata(row_pixels)
            img.paste(line_img, box)

            z_img += 1

        return img

    def rendering(self, rayHit, debug=False):

        base_color = rayHit.primitive.get_surface_color(rayHit)
        if debug:
            print(f"  [Rendering] 1. Base Color : {base_color}")

        lit_color = self._apply_lighting(rayHit, base_color, debug=debug)
        if debug:
            print(f"  [Rendering] 2. Lit Color  : {lit_color}")

        final_color = self._apply_fog(rayHit, lit_color)
        if debug:
            print(f"  [Rendering] 3. Final Color: {final_color}")

        return final_color

    def _apply_fog(self, rayHit, current_color):
        impact_time = rayHit.impact_time

        if impact_time < FOG_START:
            return current_color

        if impact_time > FOG_END:
            return self.background_color

        bg_r, bg_g, bg_b = self.background_color
        red, green, blue = current_color

        fog = (impact_time - FOG_START) / (FOG_END - FOG_START)

        inv_fog = 1 - fog

        red = int(red * inv_fog + bg_r * fog)
        green = int(green * inv_fog + bg_g * fog)
        blue = int(blue * inv_fog + bg_b * fog)

        return (red, green, blue)

    def _apply_lighting(self, rayHit, current_color, debug=False):
        rr, vv, bb = current_color
        nx, ny, nz = rayHit.world_normal
        lx, ly, lz = self.camera.light_dir

        ps = nx * lx + ny * ly + nz * lz

        if debug:
            print("\n  [Lighting Debug]")
            print(f"  ├─ Normal (N) : ({nx: 8.3f}, {ny: 8.3f}, {nz: 8.3f})")
            print(f"  ├─ Light (L)  : ({lx: 8.3f}, {ly: 8.3f}, {lz: 8.3f})")
            print(f"  ├─ Dot (N·L)  :  {ps: 8.3f}")

        if ps < 0:
            return (
                int(AMBIENT_LIGHT * rr),
                int(AMBIENT_LIGHT * vv),
                int(AMBIENT_LIGHT * bb),
            )

        diffuse = ps * 0.9

        origin_shadow = (
            rayHit.world_impact_point[0] + nx * SHADOW_BIAS,
            rayHit.world_impact_point[1] + ny * SHADOW_BIAS,
            rayHit.world_impact_point[2] + nz * SHADOW_BIAS,
        )

        shadow_ray = Ray(origin_shadow, (lx, ly, lz))

        is_occluded = self.scene.any_intersection(shadow_ray)

        if debug:
            print(
                f"  ├─ Shadow Ray : O({origin_shadow[0]:.3f}, {origin_shadow[1]:.3f}, {origin_shadow[2]:.3f}) D({lx:.3f}, {ly:.3f}, {lz:.3f})"
            )
            print(f"  ├─ Occluded ? :  {is_occluded}")

        if is_occluded:
            coef = AMBIENT_LIGHT + diffuse * (1.0 - SHADOW_OPACITY)
        else:
            coef = AMBIENT_LIGHT + diffuse

        coef = min(1.0, coef)

        return (int(coef * rr), int(coef * vv), int(coef * bb))
