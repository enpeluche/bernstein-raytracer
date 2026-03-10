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
    def __init__(self, scene, name="render", folder=""):

        self.scene = scene
        self.frame_count = 0
        self.total_time = 0
        self.name = name
        self.folder = folder

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

    def save(self, format="png", base_output="output"):
        msg = f"Frame: {self.frame_count} | Temps total d'exécution : {self.total_time:.2f} secondes"
        print(msg.ljust(50), end="\n", flush=True)

        search_pattern = os.path.join("tmp", "*.png")
        files = glob.glob(search_pattern)
        files.sort()

        if not files:
            print("Aucune image à sauvegarder.")
            return

        target_dir = (
            os.path.join(base_output, self.folder) if self.folder else base_output
        )
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)

        # --- L'AJOUT EST ICI ---
        # On récupère le nom de la caméra (ex: "demo_fisheye")
        cam_name = self.scene.camera.name

        # On crée le nom final : "nom_du_rendu_nom_de_la_camera"
        # Exemple : "test_demo_fisheye"
        final_name = f"{self.name}_{cam_name}" if cam_name else self.name
        # -----------------------

        if format == "png":
            if len(files) == 1:
                target_path = os.path.join(target_dir, f"{final_name}.png")
                shutil.copy(files[0], target_path)
            else:
                anim_dir = os.path.join(target_dir, final_name)
                if not os.path.exists(anim_dir):
                    os.makedirs(anim_dir)
                for f in files:
                    filename = os.path.basename(f)
                    shutil.copy(f, os.path.join(anim_dir, filename))

        elif format == "gif":
            frames = [Image.open(f) for f in files]
            target_path = os.path.join(target_dir, f"{final_name}.gif")

            frames[0].save(
                target_path,
                save_all=True,
                append_images=frames[1:],
                optimize=True,
                duration=60,
                loop=0,
            )
