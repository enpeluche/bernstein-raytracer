from .base import Camera
from ..Ray import Ray

from math import tan, radians


class FOVPerspectiveCamera(Camera):
    def __init__(self, *args, fov_deg=60.0, **kwargs):
        super().__init__(*args, **kwargs)
        self.fov = radians(fov_deg)
        self.focale = 1.0 / tan(self.fov / 2.0)

    def generate_ray(self, px, pz):

        u, v = self.raster_to_ndc(px, pz)

        x = u
        z = v
        y = self.focale

        origin = self.camera_to_world_point(0.0, 0.0, 0.0)
        direction = self.camera_to_world_vector(x, y, z)

        return Ray(origin=origin, direction=direction)
