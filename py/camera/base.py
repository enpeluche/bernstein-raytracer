from util import normalize3, cross
from constants import RENDER_SIZE, UP, DEG
from Matrix import Matrix
from transformation import translation, rotation_x, rotation_y, rotation_z

# -----------------------------------------------------------------------------
# CONVENTION DU REPÈRE CAMÉRA (Local Frame)
# -----------------------------------------------------------------------------
# Ce moteur utilise un repère orthonormal direct basé sur la vision :
#
#   dy : Axe OPTIQUE (Forward)  -> Direction du regard.
#   dx : Axe HORIZONTAL (Right) -> Vecteur latéral (produit UP × dy).
#   dz : Axe VERTICAL (Up)      -> Vecteur haut local (produit dy × dx).
#
# La matrice de pose stocke ces vecteurs en colonnes pour transformer
# les rayons du plan image vers l'espace du monde (World Space).
# -----------------------------------------------------------------------------


class Camera:
    """
    Représente un observateur virtuel dans l'espace 3D.

    Cette classe gère la position, l'orientation et l'éclairage global d'une scène.
    Elle utilise une matrice de pose 4x4 pour transformer l'espace du monde
    en espace caméra et définit les propriétés de rendu (résolution, échelle).

    Attributs:
        pose (Matrix): Matrice de transformation 4x4 (orientation et position).
        size_world (float): Dimension de la fenêtre de vue dans l'espace mathématique.
        size_win (int): Résolution de l'image de sortie en pixels (largeur/hauteur).
        light_dir (tuple): Vecteur unitaire pointant vers la source de lumière.
        name (str): Identifiant de la caméra pour l'exportation des fichiers.
    """

    def __init__(
        self,
        origin,
        view_direction,
        light_dir,
        name,
        size_world=1.0,
        size_win=RENDER_SIZE,
    ):
        """
        Constructeur d'une instance générique de caméra. Ne possède pas la méthode generate_ray.

        Args:
            origin (tuple[float, float, float]): La position de la caméra/ l'oeil du spectateur.
            view_direction (tuple[float, float, float]): La direction dans laquelle on regarde.
            size_world (float): La taille du monde mathématique, peut être flottant.
            size_win (int): La taille de la fenêtre, en pixel.
            light_dir (tuple[float, float, float]): La direction de la source de lumière infinie.
            name (string): Le nom de la caméra.
        """

        dy = normalize3(view_direction)

        dx = normalize3(cross(UP, dy))

        dz = cross(dy, dx)
        # fmt: off

        self.pose = Matrix(
            [
                [dx[0], dy[0], dz[0], origin[0]],
                [dx[1], dy[1], dz[1], origin[1]],
                [dx[2], dy[2], dz[2], origin[2]],
                [    0,     0,     0,         1],
            ]
        )

        # fmt: on

        self.size_world = size_world
        self.size_win = size_win
        self.light_dir = normalize3(light_dir)
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

    def set_light_direction(self, lx, ly, lz):
        """
        Définit et normalise la direction de la lumière infinie.

        Args:
            lx, ly, lz (float): Composantes du vecteur lumière.
        """

        self.light_direction = normalize3(lx, ly, lz)

    def translate(self, tx, ty, tz):
        """
        Déplace la caméra dans l'espace du monde.

        Args:
            tx, ty, tz (float): Valeurs de translation sur les axes X, Y et Z.
        Returns:
            self: L'instance de la caméra (permet le chaînage).
        """

        self.pose = self.pose * translation(tx, ty, tz).forward

        return self

    def rotate_x(self, θ=DEG):
        """
        Effectue une rotation de la caméra autour de son axe X local (Tangage).

        Args:
            θ (float): Angle de rotation en radians.
        Returns:
            self: L'instance de la caméra (permet le chaînage).
        """

        self.pose = self.pose * rotation_x(θ).forward

        return self

    def rotate_y(self, θ=DEG):
        """
        Effectue une rotation de la caméra autour de son axe Y local (Roulis).

        Args:
            θ (float): Angle de rotation en radians.
        Returns:
            self: L'instance de la caméra (permet le chaînage).
        """

        self.pose = self.pose * rotation_y(θ).forward

        return self

    def rotate_z(self, θ=DEG):
        """
        Effectue une rotation de la caméra autour de son axe Z local (Lacet).

        Args:
            θ (float): Angle de rotation en radians.
        Returns:
            self: L'instance de la caméra (permet le chaînage).
        """
        self.pose = self.pose * rotation_z(θ).forward

        return self

    def look_at(self, target=(0.0, 0.0, 0.0)):
        """
        Réoriente la caméra pour qu'elle fixe un point précis sans changer de position.

        Args:
            target (tuple, optional): Coordonnées (x, y, z) du point cible.
                                      Par défaut l'origine du monde (0,0,0).
        Returns:
            self: L'instance de la caméra (permet le chaînage).
        """

        origin = (self.pose[0, 3], self.pose[1, 3], self.pose[2, 3])

        dy = normalize3(
            (target[0] - origin[0], target[1] - origin[1], target[2] - origin[2])
        )

        dx = normalize3(cross(UP, dy))

        dz = cross(dy, dx)

        # fmt: off

        self.pose = Matrix(
            [
                [dx[0], dy[0], dz[0], origin[0]],
                [dx[1], dy[1], dz[1], origin[1]],
                [dx[2], dy[2], dz[2], origin[2]],
                [    0,     0,     0,         1],
            ]
        )

        # fmt: on

    def camera_to_world_point(self, x, y, z):
        """
        Transforme un point de l'espace local caméra vers l'espace monde.
        Le point subit la rotation ET la translation (composante w=1).
        """
        # Utilisation d'une matrice colonne (point homogène)
        p_local = Matrix([[x], [y], [z], [1.0]])
        p_world = self.pose * p_local

        # On retourne un tuple (x, y, z) pour la compatibilité avec Ray
        return (p_world[0, 0], p_world[1, 0], p_world[2, 0])

    def camera_to_world_vector(self, x, y, z):
        """
        Transforme un vecteur de l'espace local caméra vers l'espace monde.
        Le vecteur ne subit QUE la rotation (composante w=0).
        """
        # Utilisation d'une matrice colonne (vecteur homogène)
        v_local = Matrix([[x], [y], [z], [0.0]])
        v_world = self.pose * v_local

        # On retourne un tuple (x, y, z)
        return (v_world[0, 0], v_world[1, 0], v_world[2, 0])

    def raster_to_ndc(self, px, pz):
        """
        Transforme les coordonnées discrètes des pixels (Raster Space) en
        coordonnées normalisées continues (Normalized Device Coordinates).

        Cette méthode projette l'indice du pixel sur un plan cartésien centré,
        permettant de passer d'une grille [0, N-1] au carré unitaire [-1, 1]^2.
        L'ajout de 0.5 permet de lancer le rayon depuis le CENTRE du pixel.

        Args:
            px (int): Indice de colonne du pixel (0 à size_win - 1).
            pz (int): Indice de ligne du pixel (0 à size_win - 1).

        Returns:
            tuple[float, float]: Coordonnées (u, v) dans l'espace NDC,
                                 comprises dans l'intervalle [-1, 1] x [-1, 1].
        """
        N = self.size_win

        u = (px + 0.5) / N
        v = (pz + 0.5) / N

        u = 2 * u - 1
        v = 2 * v - 1

        return u, v
