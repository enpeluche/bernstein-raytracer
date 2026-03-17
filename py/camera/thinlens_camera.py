from .base import Camera
from Ray import Ray

from math import tan, cos, sin, sqrt, pi, radians
import random
from util import normalize3


class ThinLensCamera(Camera):
    def __init__(self, *args, fov_deg=60, aperture=0.1, focus_dist=5.0, **kwargs):
        super().__init__(*args, **kwargs)
        self.fov = radians(fov_deg)
        self.focale = 1.0 / tan(self.fov / 2.0)
        self.aperture = aperture
        self.focus_dist = focus_dist

    def random_disk(self):
        r = sqrt(random.random())
        theta = 2 * pi * random.random()
        return r * cos(theta), r * sin(theta)

    def generate_ray(self, px, pz):

        u, v = self.raster_to_ndc(px, pz)

        x = u
        z = v
        y = self.focale

        # rayon idéal
        dir_local = normalize3((x, y, z))

        # point focal
        focus_point = (
            dir_local[0] * self.focus_dist,
            dir_local[1] * self.focus_dist,
            dir_local[2] * self.focus_dist,
        )

        # échantillon ouverture
        dx, dz = self.random_disk()
        dx *= self.aperture
        dz *= self.aperture

        origin_local = (dx, 0.0, dz)

        direction_local = (
            focus_point[0] - origin_local[0],
            focus_point[1] - origin_local[1],
            focus_point[2] - origin_local[2],
        )

        origin = self.camera_to_world_point(*origin_local)
        direction = self.camera_to_world_vector(*direction_local)

        return Ray(origin=origin, direction=direction)
