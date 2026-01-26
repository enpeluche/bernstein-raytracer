import pygame
import time

from main import *  # Ton moteur
from Cameras import CameraPerspective
from util import normalize3
from DAG import *  # Important pour la vitesse
from Object3D import *  # Tes objets
from Object import *
from Renderer import *

# --- PARAMÈTRES ---
W_FENETRE = 500
H_FENETRE = 500

# Résolution du rendu (Plus c'est petit, plus c'est fluide/pixelisé)
# 80x60 pixels = Très fluide
# 200x150 pixels = Plus joli mais lent
RES_W = 500
RES_H = 500


def scene_tunnel():
    b3 = Prim(boule(0, 0, 4, 1.0), (0, 0, 255), AABB((-1, -1, -1 + 4), (1, 1, 1 + 4)))

    return b3


def main():
    pygame.init()
    screen = pygame.display.set_mode((W_FENETRE, H_FENETRE))
    pygame.display.set_caption("Raytracer Temps Réel - Python")
    clock = pygame.time.Clock()

    # --- INITIALISATION CAMERA ---
    # On stocke la position et la rotation
    cam_pos = [0.0, 0.0, -5.0]
    soleil_dir = [-1.0, 0.0, -0.5]

    # Surface temporaire pour le rendu basse résolution
    surface_rendu = pygame.Surface((RES_W, RES_H))

    running = True
    scene = scene_tunnel()

    print("--- COMMANDES ---")
    print("Flèches : Bouger (X/Z)")
    print("PageUp/Down : Monter/Descendre (Y)")
    print("-----------------")

    while running:
        # 1. GESTION DES ÉVÉNEMENTS (Clavier/Souris)
        # 1. GESTION DES ÉVÉNEMENTS
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # --- AJOUT DU SCROLL SOURIS ---
            elif event.type == pygame.MOUSEWHEEL:
                # event.y vaut 1 quand on scrolle vers le haut, -1 vers le bas
                sensibilite_scroll = 1.0
                cam_pos[2] += event.y * sensibilite_scroll

        keys = pygame.key.get_pressed()
        vitesse = 0.1

        # Déplacement simple
        if keys[pygame.K_LEFT]:
            cam_pos[0] -= vitesse
        if keys[pygame.K_RIGHT]:
            cam_pos[0] += vitesse
        if keys[pygame.K_UP]:
            cam_pos[1] += vitesse
        if keys[pygame.K_DOWN]:
            cam_pos[1] -= vitesse

        if keys[pygame.K_z]:
            soleil_dir[0] -= vitesse
        if keys[pygame.K_s]:
            soleil_dir[0] += vitesse
        if keys[pygame.K_q]:
            soleil_dir[1] -= vitesse
        if keys[pygame.K_d]:
            soleil_dir[1] += vitesse

        cam = CameraPerspective(
            tuple(cam_pos),
            (1.0, 0.0, 0.0),
            normalize3((0.3, 0.2, 1.0)),
            (0.0, 1.0, 0.0),
            1.5,
            RES_W,
            normalize3(tuple(soleil_dir)),
            "action_shot.png",
            focale=2.0,
        )

        cam.h = RES_H
        pixels = raycasting_buffer(cam, scene)

        px_array = pygame.PixelArray(surface_rendu)
        for y in range(RES_H):
            for x in range(RES_W):
                # Récupérer la couleur (r, g, b)
                # Attention: raycasting renvoie souvent une liste plate ou liste de listes
                idx = y * RES_W + x
                color = pixels[idx]
                px_array[x, y] = color  # x, y inversés parfois selon libs
        del px_array  # Déverrouiller la surface

        # 5. ÉTIREMENT ET AFFICHAGE FINAL
        # On agrandit la petite image floue pour remplir la fenêtre
        pygame.transform.scale(surface_rendu, (W_FENETRE, H_FENETRE), screen)
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
