from PIL import Image, ImageDraw, ImageFont
from util import clamp
import time
import random
from Ray import Ray

_worker_cam = None
_worker_scene = None


def _init_worker(cam, scene):
    """Initialise la mémoire partagée pour chaque processus."""
    global _worker_cam, _worker_scene
    _worker_cam = cam
    _worker_scene = scene


def _process_line(y):
    """Fonction exécutée par les workers pour calculer une ligne de l'image."""

    cam = _worker_cam
    scene = _worker_scene

    width = 2 * cam.size_win + 1

    py = (height / 2.0) - y

    ligne_pixels = []
    for x in range(width):
        px = x - (width / 2.0)
        rayon = cam.generate_ray(px, py)
        intervalles = scene.intersection(rayon)

        color = (0, 0, 0)
        if intervalles:
            hit = None
            for contact in intervalles:
                if contact.a.t > 0:
                    hit = contact.a
                    break
            if hit:
                color = rendering(cam, hit)
        ligne_pixels.append(color)
    return ligne_pixels


def rendering(cam, contact, scene):
    (rr, vv, bb) = contact.color
    (nx, ny, nz, d) = contact.plan
    (lx, ly, lz) = cam.light_dir

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
        contact.pt[0] + nx * epsilon,
        contact.pt[1] + ny * epsilon,
        contact.pt[2] + nz * epsilon,
    )

    shadow_ray = Ray(origin_shadow, (lx, ly, lz))

    obstacles = scene.intersection(shadow_ray)

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


class Renderer:
    def __init__(self):
        pass


def raycasting(cam, scene):
    start = time.perf_counter()

    print("Début de génération de l'image.")

    pixels_buffer = []

    for zpix in range(cam.size_win, -cam.size_win - 1, -1):
        for xpix in range(-cam.size_win, cam.size_win + 1):
            rayon = cam.generate_ray(xpix, zpix)
            intervalles = scene.intersection(rayon)

            if [] == intervalles or intervalles == None:
                (r, v, b) = cam.background_color
            # elif intervalles[0].a.t > 10: # fog ?
            #    (r, v, b) = cam.background_color
            else:
                (r, v, b) = rendering(cam, intervalles[0].a, scene)

            pixels_buffer.append((r, v, b))

    img = Image.new("RGB", (2 * cam.size_win + 1, 2 * cam.size_win + 1))
    img.putdata(pixels_buffer)
    img.save("render.png")
    end = time.perf_counter()
    print(f"Temps d'exécution : {end - start:.6f} secondes")


def raycasting_buffer(cam, scene):

    width = cam.h
    height = cam.h
    buffer = []

    hx = width / 2.0
    hz = height / 2.0

    for y in range(height):

        py = hz - y
        for x in range(width):
            px = x - hx

            rayon = cam.generate_ray(px, py)

            intervalles = scene.intersection(rayon)

            col = (0, 0, 0)
            if intervalles:
                hit = intervalles[0].a
                if hit.t > 0:

                    col = rendering(cam, hit)

            buffer.append(col)

    return buffer


def calcul_ligne_optimise(y):
    """
    Maintenant, cette fonction ne prend que 'y'.
    Elle utilise les variables globales initialisées ci-dessus.
    """
    cam = worker_cam
    scene = worker_scene

    width = 2 * cam.size_win + 1
    height = 2 * cam.size_win + 1
    py = (height / 2.0) - y

    bg_color = cam.background_color
    ligne_pixels = []

    for x in range(width):
        px = x - (width / 2.0)
        rayon = cam.generate_ray(px, py)
        intervalles = scene.intersection(rayon)

        final_color = bg_color
        if intervalles:
            hit = None
            for contact in intervalles:
                if contact.a.t > 0.001:
                    hit = contact.a
                    break
            if hit:
                obj_color = rendering(cam, hit)
                final_color = obj_color

        ligne_pixels.append(final_color)

    return ligne_pixels


def raycasting_parallele(cam, scene):
    print(f"émarrage MP Optimisé sur {mp.cpu_count()} cœurs...")
    start = time.perf_counter()

    height = 2 * cam.size_win + 1

    tâches = range(height)

    with mp.Pool(
        processes=mp.cpu_count(), initializer=init_worker, initargs=(cam, scene)
    ) as pool:

        resultats = pool.map(calcul_ligne_optimise, tâches, chunksize=50)

    buffer_final = [pixel for ligne in resultats for pixel in ligne]

    end = time.perf_counter()
    print(f" Rendu terminé en {end - start:.4f} secondes")

    img = Image.new("RGB", (2 * cam.size_win + 1, 2 * cam.size_win + 1))
    img.putdata(buffer_final)
    img.save("render_para_opti.png")

    return buffer_final


def raycasting_antialiasing(cam, scene, samples=4):
    # ... (début de ta boucle habituelle)
    for y in range(500):
        for x in range(500):
            total_r, total_g, total_b = 0, 0, 0

            for s in range(samples):

                dx = random.uniform(-0.5, 0.5)
                dz = random.uniform(-0.5, 0.5)

                rayon = cam.generate_ray(x + dx, z + dz)
                couleur = calculer_couleur_rayon(rayon, scene)

                total_r += couleur[0]
                total_g += couleur[1]
                total_b += couleur[2]

            # On fait la moyenne
            final_color = (total_r // samples, total_g // samples, total_b // samples)
            buffer.append(final_color)
