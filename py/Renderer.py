from PIL import Image, ImageDraw, ImageFont
from util import clamp
import time
import random
from Ray import Ray
import os
import shutil
import glob

# faire une classe Scene et une classe Renderer (fichier temporaire, mais au moins, on aura moins de ram)


class Renderer:
    def __init__(self, scene):

        self.scene = scene
        self.frame_count = 0

        if os.path.exists("tmp"):
            shutil.rmtree("tmp")
        os.makedirs("tmp")

    def render(self):
        frame = self.scene.raycasting()

        frame.save(f"tmp/{self.frame_count:04d}.png")

        self.frame_count += 1

    def save(self, format="png"):
        if format == "png":
            pass

        if format == "gif":

            search_pattern = os.path.join("tmp", "*.png")
            files = glob.glob(search_pattern)

            files.sort()

            if not files:
                print("⚠️ Aucune image trouvée dans le dossier temporaire !")
                return

            print(f"🎞️ Assemblage de {len(files)} images...")

            frames = [Image.open(f) for f in files]

            frames[0].save(
                "mon_film.gif",
                save_all=True,
                append_images=frames[1:],  # On accroche les wagons
                optimize=True,
                duration=100,
                loop=0,
            )

        print("✅ GIF terminé : mon_film.gif")

        # 5. (Optionnel) Nettoyage
        # Tu peux supprimer le dossier temporaire ici si tu veux faire le ménage
        # import shutil
        # shutil.rmtree(self.temp_dir)


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
