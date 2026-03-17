from .base import Camera
from Ray import Ray

from math import sin, cos, sqrt, radians, atan2


class FisheyeCamera(Camera):
    def __init__(self, *args, fov_deg=180.0, **kwargs):
        super().__init__(*args, **kwargs)
        self.theta_max = radians(fov_deg) / 2.0

    def generate_ray(self, px, pz):

        u, v = self.raster_to_ndc(px, pz)

        r = sqrt(u * u + v * v)

        if r > 1:
            return None  # hors du cercle image

        theta = r * self.theta_max
        phi = atan2(v, u)

        x = sin(theta) * cos(phi)
        z = sin(theta) * sin(phi)
        y = cos(theta)

        origin = self.camera_to_world_point(0.0, 0.0, 0.0)
        direction = self.camera_to_world_vector(x, y, z)

        return Ray(origin=origin, direction=direction)
