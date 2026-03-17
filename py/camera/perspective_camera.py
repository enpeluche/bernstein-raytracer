from .base import Camera
from Ray import Ray
from util import normalize3
from constants import RENDER_SIZE

# 1.0 = Grand angle (type GoPro)
# 2.0 = Vue standard (humain)
# 5.0 = Zoom (Téléobjectif)


class PerspectiveCamera(Camera):
    """
    PerspectiveCamera simule l'oeil humain en fixant l'origine du rayon mais faisant varier sa direction.
    """

    def __init__(
        self,
        origin,
        view_direction,
        light_dir,
        name,
        focale=2.0,
        size_world=1.0,
        size_win=RENDER_SIZE,
    ):
        """
        Constructeur d'une instance de PerspectiveCamera.

        Args:
            pose (tuple[float, float, float]): La position de la caméra.
            cam_dx (tuple[float, float, float]): La direction de la caméra sur l'axe x.
            cam_dy (tuple[float, float, float]): La direction de la caméra sur l'axe y.
            cam_dz (tuple[float, float, float]): La direction de la caméra sur l'axe z.
            size_world (float): La taille du monde mathématique, peut être flottant.
            size_win (int): La taille de la fenêtre, en pixel.
            light_dir (tuple[float, float, float]): La direction de la source de lumière infinie.
            name (string): Le nom de la caméra.
            focal (float):
        """

        super().__init__(origin, view_direction, light_dir, name, size_world, size_win)
        self.focale = float(focale)

    def generate_ray(self, px, pz):
        """
        Args:
            px (int): L'abscice du pixel que l'on veut calculer.
            pz (int): L'ordonnée du pixel que l'on veut calculer.
        """
        u, v = self.raster_to_ndc(px, pz)

        x = u * self.size_world / 2
        y = self.focale
        z = v * self.size_world / 2

        # On place le point sur le plan image local et on le projette dans le monde
        origin = (self.pose[0, 3], self.pose[1, 3], self.pose[2, 3])

        # Pour une caméra ortho, tous les rayons vont vers l'avant (Forward = dy local)
        direction = self.camera_to_world_vector(x, y, z)

        return Ray(origin=origin, direction=direction)
