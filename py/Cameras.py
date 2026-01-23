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
        Docstring for __init__

        :param self: Description
        :param cam_o: Description
        :param cam_dx: Description
        :param cam_dy: Description
        :param cam_dz: Description
        :param size_world: Description
        :param size_win: Description
        :param light_dir: Description
        :param name: Description
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
        Docstring for generate_ray

        :param self: Description
        :param px: Description
        :param pz: Description
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
            direction=self.oy,
        )


class CameraPerspective:
    """
    Docstring for CameraPerspective
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
        Docstring for __init__

        :param self: Description
        :param cam_o: Description
        :param cam_dx: Description
        :param cam_dy: Description
        :param cam_dz: Description
        :param size_world: Description
        :param size_win: Description
        :param light_dir: Description
        :param name: Description
        :param focale: Description
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
        self.focale = float(focale)

    def generate_ray(self, px, pz):
        """
        Docstring for generate_ray

        :param self: Description
        :param px: Description
        :param pz: Description
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
