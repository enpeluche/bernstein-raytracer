from Rayon import Rayon
from util import *

class CameraPerspective(object):
    def __init__(self, o, ox, oy, oz, hsizeworld, hsizewin, soleil, nom, focale=2.0):
        self.o = o
        self.ox = ox  # Vecteur Droite (X écran)
        self.oy = oy  # Vecteur Devant (Direction du regard)
        self.oz = oz  # Vecteur Haut (Y écran)
        self.hsizeworld = hsizeworld
        self.hsizewin = hsizewin
        self.soleil = normalize3(soleil)
        self.background = (44, 55, 88)
        self.nom = nom
        self.focale = float(focale)  # Distance entre l'oeil et l'écran virtuel

    def generate_ray(self, x, z):
        # 1. Calcul de la position du pixel sur l'écran virtuel
        # L'écran est situé à une distance 'focale' devant l'oeil

        # Coordonnées locales sur l'écran
        u = interpole(0.0, 0.0, self.hsizewin, self.hsizeworld, float(x))
        v = interpole(0.0, 0.0, self.hsizewin, self.hsizeworld, float(z))

        # 2. Construction du vecteur direction
        # Direction = (Point sur l'écran) - (Position de l'oeil)
        # Mais mathématiquement, c'est simplement :
        # Focale * DEVANT + u * DROITE + v * HAUT

        dx = self.focale * self.oy[0] + u * self.ox[0] + v * self.oz[0]
        dy = self.focale * self.oy[1] + u * self.ox[1] + v * self.oz[1]
        dz = self.focale * self.oy[2] + u * self.ox[2] + v * self.oz[2]

        # 3. IMPORTANT : Il faut normaliser la direction pour le Raymarching
        direction_normalisee = normalize3((dx, dy, dz))

        # 4. Le rayon part de l'OEIL (fixe) avec la direction calculée
        return Rayon(self.o, direction_normalisee)