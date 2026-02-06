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
        self.total_time = 0

        if os.path.exists("tmp"):
            shutil.rmtree("tmp")
        os.makedirs("tmp")

    def render(self):
        msg = f"              Frame: {self.frame_count} | Temps total d'exécution : {self.total_time} secondes"

        # print(msg.ljust(50), end="\r", flush=True)

        start = time.perf_counter()
        frame = self.scene.raycasting()
        end = time.perf_counter()

        self.total_time += end - start

        frame.save(f"tmp/{self.frame_count:04d}.png")

        self.frame_count += 1

    def save(self, format="png"):
        msg = f"Frame: {self.frame_count} | Temps total d'exécution : {self.total_time} secondes"

        print(msg.ljust(50), end="\n", flush=True)
        if format == "png":
            pass

        if format == "gif":

            search_pattern = os.path.join("tmp", "*.png")
            files = glob.glob(search_pattern)

            files.sort()

            if not files:
                return

            frames = [Image.open(f) for f in files]

            frames[0].save(
                "mon_film.gif",
                save_all=True,
                append_images=frames[1:],
                optimize=True,
                duration=100,
                loop=0,
            )
