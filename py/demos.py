from constants import DEG, white
from Cameras import CameraPerspective
from Scene import Scene
from Shapes import *

perspective_camera = CameraPerspective(
    cam_o=(0.0, -3, 0.0),
    cam_dx=(1.0, 0.0, 0.0),
    cam_dy=(0.0, 1.0, 0.0),  # la direction des rayons aussi
    cam_dz=(0.0, 0.0, 1.0),
    size_world=1,
    size_win=1000,
    light_dir=(1, -2, 0.75),
    name="",
    focale=1.0,
)

P2 = Plane(color=white).rotate_x(90 * DEG).translate(0, 5, 0)

S = Sphere(1, color=(240, 47, 79), apply_grid_pattern=True)


def demo_sphere_perspective():
    perspective_camera.cam_o = (0.0, -2.5, 0.0)
    perspective_camera.light_dir = normalize3((1, -2.25, 0.5))
    return Scene(perspective_camera, P2 + S)


T = Tore(0.2, 0.8, color=(240, 47, 79), apply_grid_pattern=True)


def demo_torus_perspective():
    perspective_camera.cam_o = (0.0, -3, 0.0)
    perspective_camera.light_dir = normalize3((1, -2, 1))
    return Scene(perspective_camera, P2 + T)


H1 = HyperboloidOneSheet(color=(240, 47, 79), apply_grid_pattern=True)


def demo_hyperboloidonesheet_perspective():
    return Scene(perspective_camera, P2 + H1)


H2 = HyperboloidTwoSheets(color=(240, 47, 79), apply_grid_pattern=True)


def demo_hyperboloidtwosheets_perspective():
    return Scene(perspective_camera, P2 + H2)


R = Roman(color=(240, 47, 79), apply_grid_pattern=True)


def demo_roman_perspective():
    return Scene(perspective_camera, P2 + R)


C = Caylay(color=(240, 47, 79), apply_grid_pattern=True).scale(0.4, 0.4, 0.4)


def demo_caylay_perspective():
    return Scene(perspective_camera, P2 + C)


S2 = Steiner2(color=(240, 47, 79), apply_grid_pattern=True)


def demo_steiner2_perspective():
    return Scene(perspective_camera, P2 + S2)


S4 = Steiner4(color=(240, 47, 79), apply_grid_pattern=True).rotate_z(DEG * 30)


def demo_steiner4_perspective():
    return Scene(perspective_camera, P2 + S4)


W = WhitneyUmbrella(color=(240, 47, 79), apply_grid_pattern=True)


def demo_whitney_umbrella_perspective():
    return Scene(perspective_camera, P2 + W)


objet_csg_0 = R - S.scale(0.7, 0.7, 0.7)
objet_csg_1 = H1 & T.scale(1.25, 1.25, 1.25)
C2 = (
    Caylay(color=(240, 47, 79), apply_grid_pattern=True)
    .scale(0.4, 0.4, 0.4)
    .rotate_z(90 * DEG)
)
objet_csg_2 = (C + C2) & S


# Deux grandes sphères décalées sur l'axe X
S_gauche = Sphere(1.0, color=(100, 200, 255), apply_grid_pattern=True).translate(
    -0.6, 0, 0
)
S_droite = Sphere(1.0, color=(100, 200, 255), apply_grid_pattern=True).translate(
    0.6, 0, 0
)

# L'intersection crée une lentille biconvexe (comme une loupe)
lentille = S_gauche & S_droite

# On la pose sur un plan pour voir l'ombre
scene_lentille = P2 + lentille

# --- 1. Le Bloc Principal ---
# Le cylindre infini de base
cyl_infini = Cylindre(0.55, color=(150, 150, 150), apply_grid_pattern=True)
# La sphère qui va "boucher" le haut et le bas (Intersection)
boite_coupe = Sphere(0.75)

barillet_base = cyl_infini & boite_coupe

# --- 2. Le Trou Central ---
# Un petit cylindre pour l'axe de rotation
trou_central = Cylindre(0.1, apply_grid_pattern=True)

# --- 3. Les 6 Chambres ---
r_chambre = 0.15
d = 0.33  # Distance entre le centre du barillet et le centre d'une chambre

# Regarde comme tes transformations rendent ça propre :
t0 = Cylindre(r_chambre, apply_grid_pattern=True).translate(d, 0, 0)
t1 = Cylindre(r_chambre, apply_grid_pattern=True).translate(d, 0, 0).rotate_z(60 * DEG)
t2 = Cylindre(r_chambre, apply_grid_pattern=True).translate(d, 0, 0).rotate_z(120 * DEG)
t3 = Cylindre(r_chambre, apply_grid_pattern=True).translate(d, 0, 0).rotate_z(180 * DEG)
t4 = Cylindre(r_chambre, apply_grid_pattern=True).translate(d, 0, 0).rotate_z(240 * DEG)
t5 = Cylindre(r_chambre, apply_grid_pattern=True).translate(d, 0, 0).rotate_z(300 * DEG)

# --- 4. La Sculpture Finale (CSG) ---
# On prend la base, et on soustrait TOUT le reste
barillet = barillet_base - trou_central - t0 - t1 - t2 - t3 - t4 - t5

# --- 5. Mise en scène ---
# On incline le barillet pour bien voir à travers les trous
barillet.rotate_x(45 * DEG).rotate_y(30 * DEG)

# On ajoute un plan de sol en dessous pour voir l'ombre spectaculaire
sol = Plane(color=white, apply_grid_pattern=False).translate(0, 0, -1.5)


soleil = Sphere(0.5, color=(255, 200, 0), apply_grid_pattern=False)

# On crée une planète, on l'éloigne de 2 unités, PUIS on tourne la scène complète dans l'animation
planete = Sphere(0.2, color=(100, 100, 255), apply_grid_pattern=False)
planete.translate(2.0, 0.0, 0.0)


# 1. On fabrique notre "cœur de Romaine" classique
R = Roman(color=(240, 47, 79), apply_grid_pattern=True)
S = Sphere(0.8, color=(240, 47, 79), apply_grid_pattern=True)
coeur_roman = R - S

# 2. ON TRANSFORME LE BLOC ENTIER
# On l'aplatit légèrement, on le tourne, on le lève
coeur_roman.scale(1.0, 0.5, 1.0).rotate_z(30 * DEG).translate(0, 1.0, 0)

# 3. On ajoute un sol pour voir l'ombre portée de ce nouvel objet muté
sol = Plane(color=(200, 200, 200), apply_grid_pattern=True).translate(0, -2, 0)
