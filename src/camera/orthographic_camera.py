from .base import Camera
from ..Ray import Ray


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
        u, v = self.raster_to_ndc(px, pz)

        x = u * self.size_world / 2
        y = 0.0
        z = v * self.size_world / 2

        # On place le point sur le plan image local et on le projette dans le monde
        origin = self.camera_to_world_point(x, y, z)

        # Pour une caméra ortho, tous les rayons vont vers l'avant (Forward = dy local)
        direction = self.camera_to_world_vector(0.0, 1.0, 0.0)  # et pas dy justement?

        return Ray(origin=origin, direction=direction)
