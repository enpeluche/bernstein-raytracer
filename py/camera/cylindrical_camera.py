from .base import Camera
from Ray import Ray

from math import sin, cos, radians


class CylindricalCamera(Camera):
    def __init__(self, *args, fov_deg=180.0, **kwargs):
        super().__init__(*args, **kwargs)
        self.theta_max = radians(fov_deg)

    def generate_ray(self, px, pz):

        u, v = self.raster_to_ndc(px, pz)

        theta = u * self.theta_max / 2.0

        x = sin(theta)
        y = cos(theta)
        z = v

        origin = self.camera_to_world_point(0.0, 0.0, 0.0)
        direction = self.camera_to_world_vector(x, y, z)

        return Ray(origin=origin, direction=direction)
