from Ray import Ray
from util import interpole, normalize3


class Camera:
    """
    Docstring for Camera
    """

    def __init__(
        self, cam_o, cam_dx, cam_dy, cam_dz, size_world, size_win, light_dir, name
    ):
        """
        Constructeur d'une instance générique de caméra. Ne possède pas la méthode generate_ray.

        Args:
            cam_o (tuple[float, float, float]): La position de la caméra.
            cam_dx (tuple[float, float, float]): La direction de la caméra sur l'axe x.
            cam_dy (tuple[float, float, float]): La direction de la caméra sur l'axe y.
            cam_dz (tuple[float, float, float]): La direction de la caméra sur l'axe z.
            size_world (float): La taille du monde mathématique, peut être flottant.
            size_win (int): La taille de la fenêtre, en pixel.
            light_dir (tuple[float, float, float]): La direction de la source de lumière infinie.
            name (string): Le nom de la caméra.
        """
        self.cam_o = cam_o
        self.cam_dx = cam_dx
        self.cam_dy = cam_dy
        self.cam_dz = cam_dz
        self.size_world = size_world
        self.size_win = size_win
        self.light_dir = normalize3(light_dir)
        self.background_color = (44, 55, 88)
        self.name = name

    def generate_ray(self, px, pz):
        """
        Méthode abstraite devant être redéfinie par les sous-classes.

        Args:
            px (int): L'abscice du pixel que l'on veut calculer.
            pz (int): L'ordonnée du pixel que l'on veut calculer.
        """
        raise NotImplementedError(
            "La classe de base Camera ne peut pas génerer de rayons."
        )

    def transform(self, T_o, T_dx, T_dy, T_dz, T_light_dir):
        """"""


class OrthographicCamera(Camera):
    """
    OrthographicCamera fixe la direction des rayons, mais fait varier leurs origines.
    """

    def generate_ray(self, px, pz):
        """
        Docstring for generate_ray

        Args:
            px (int): L'abscice du pixel que l'on veut calculer.
            pz (int): L'ordonnée du pixel que l'on veut calculer.
        """
        world_x = interpole(0.0, 0.0, self.size_win, self.size_world, float(px))
        world_z = interpole(0.0, 0.0, self.size_win, self.size_world, float(pz))

        (cam_ox, cam_oy, cam_oz) = self.cam_o

        return Ray(
            origin=(
                cam_ox + world_x * self.cam_dx[0] + world_z * self.cam_dz[0],
                cam_oy + world_x * self.cam_dx[1] + world_z * self.cam_dz[1],
                cam_oz + world_x * self.cam_dx[2] + world_z * self.cam_dz[2],
            ),
            direction=self.cam_dy,
        )


# 1.0 = Grand angle (type GoPro)
# 2.0 = Vue standard (humain)
# 5.0 = Zoom (Téléobjectif)
class CameraPerspective(Camera):
    """
    CameraPerspective simule l'oeil humain en fixant l'origine du rayon mais faisant varier sa direction.
    """

    def __init__(
        self,
        cam_o,
        cam_dx,
        cam_dy,
        cam_dz,
        size_world,
        size_win,
        light_dir,
        name,
        focale=2.0,
    ):
        """
        Constructeur d'une instance de CameraPerspective.

        Args:
            cam_o (tuple[float, float, float]): La position de la caméra.
            cam_dx (tuple[float, float, float]): La direction de la caméra sur l'axe x.
            cam_dy (tuple[float, float, float]): La direction de la caméra sur l'axe y.
            cam_dz (tuple[float, float, float]): La direction de la caméra sur l'axe z.
            size_world (float): La taille du monde mathématique, peut être flottant.
            size_win (int): La taille de la fenêtre, en pixel.
            light_dir (tuple[float, float, float]): La direction de la source de lumière infinie.
            name (string): Le nom de la caméra.
            focal (float):
        """

        super().__init__(
            cam_o, cam_dx, cam_dy, cam_dz, size_world, size_win, light_dir, name
        )
        self.focale = float(focale)

    def generate_ray(self, px, pz):
        """
        Args:
            px (int): L'abscice du pixel que l'on veut calculer.
            pz (int): L'ordonnée du pixel que l'on veut calculer.
        """
        world_x = interpole(0.0, 0.0, self.size_win, self.size_world, float(px))
        world_z = interpole(0.0, 0.0, self.size_win, self.size_world, float(pz))

        dx = (
            self.focale * self.cam_dy[0]
            + world_x * self.cam_dx[0]
            + world_z * self.cam_dz[0]
        )
        dy = (
            self.focale * self.cam_dy[1]
            + world_x * self.cam_dx[1]
            + world_z * self.cam_dz[1]
        )
        dz = (
            self.focale * self.cam_dy[2]
            + world_x * self.cam_dx[2]
            + world_z * self.cam_dz[2]
        )

        return Ray(origin=self.cam_o, direction=normalize3((dx, dy, dz)))
