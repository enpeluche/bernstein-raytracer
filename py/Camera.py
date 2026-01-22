from Rayon import Rayon
from util import *
class Camera(object):
    def __init__(self, o, ox, oy, oz, hsizeworld, hsizewin, soleil, nom):
        self.o = o
        self.ox = ox  # vers la droite du spectateur
        self.oy = oy  # regard du spectateur
        self.oz = oz  # vertical du spectateur
        self.hsizeworld = hsizeworld
        self.hsizewin = hsizewin
        self.soleil = normalize3(soleil)
        self.background = (44, 55, 88)
        self.nom = nom

    def generate_ray(self, x, z):
        (x0, y0, z0) = self.o

        kx = interpole(0.0, 0.0, self.hsizewin, self.hsizeworld, float(x))
        kz = interpole(0.0, 0.0, self.hsizewin, self.hsizeworld, float(z))

        return Rayon(
            (
                x0 + kx * self.ox[0] + kz * self.oz[0],
                y0 + kx * self.ox[1] + kz * self.oz[1],
                z0 + kx * self.ox[2] + kz * self.oz[2],
            ),
            self.oy,
        )