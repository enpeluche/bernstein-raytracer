from constants import DEG, white
from Cameras import CameraPerspective, OrthographicCamera
from Scene import Scene
from Shapes import *
from Renderer import *

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

orthographic_camera = OrthographicCamera(
    cam_o=(0.0, -3, 0.0),
    cam_dx=(1.0, 0.0, 0.0),
    cam_dy=(0.0, 1.0, 0.0),  # la direction des rayons aussi
    cam_dz=(0.0, 0.0, 1.0),
    size_world=2,
    size_win=500,
    light_dir=(1, -2, 0.75),
    name="",
)

P2 = Plane(color=white).rotate_x(90 * DEG).translate(0, 5, 0)


def demo_sphere():
    print("Démo : Sphère (Perspective vs Orthographique)")

    S = Sphere(1, color=(240, 47, 79), apply_grid_pattern=True)
    world = P2 + S

    # ==========================================
    # PERSPECTIVE
    # ==========================================

    perspective_camera.cam_o = (0.0, -2.5, 0.0)
    perspective_camera.light_dir = normalize3((1, -2.25, 0.5))

    scene_persp = Scene(perspective_camera, world)
    renderer_persp = Renderer(scene_persp, name="sphere_perspective", folder="sphere")

    renderer_persp.render()
    renderer_persp.save(format="png")

    # ==========================================
    # ORTHOGRAPHIC
    # ==========================================

    S.apply_grid_pattern = False

    orthographic_camera.light_dir = normalize3((1, -2.25, 0.5))

    scene_orthographic = Scene(orthographic_camera, world)
    renderer_orthographic = Renderer(
        scene_orthographic, name="sphere_orthographic", folder="sphere"
    )

    renderer_orthographic.render()
    renderer_orthographic.save(format="png")


def demo_torus():
    print("Démo : Tore (Perspective vs Orthographique)")

    T = Tore(0.2, 0.8, color=(240, 47, 79), apply_grid_pattern=True)
    world = P2 + T

    # ==========================================
    # PERSPECTIVE
    # ==========================================

    scene_perspective = Scene(perspective_camera, world)

    renderer_persp = Renderer(
        scene_perspective, name="torus_perspective", folder="torus"
    )

    renderer_persp.render()
    renderer_persp.save(format="png")

    # ==========================================
    # ORTHOGRAPHIC
    # ==========================================

    T.apply_grid_pattern = False

    scene_orthographic = Scene(orthographic_camera, world)

    renderer_orthographic = Renderer(
        scene_orthographic, name="torus_orthographic", folder="torus"
    )

    renderer_orthographic.render()
    renderer_orthographic.save(format="png")


def demo_hyperboloidonesheet():
    print("Démo : Hyperboloïde à une nappe (Perspective vs Orthographique)")

    H1 = HyperboloidOneSheet(color=(240, 47, 79), apply_grid_pattern=True)
    world = P2 + H1
    # ==========================================
    # PERSPECTIVE
    # ==========================================

    scene_perspective = Scene(perspective_camera, world)

    renderer_persp = Renderer(
        scene_perspective,
        name="hyperboloidonesheet_perspective",
        folder="hyperboloidonesheet",
    )

    renderer_persp.render()
    renderer_persp.save(format="png")

    # ==========================================
    # ORTHOGRAPHIC
    # ==========================================

    H1.apply_grid_pattern = False

    scene_orthographic = Scene(orthographic_camera, world)

    renderer_orthographic = Renderer(
        scene_orthographic,
        name="hyperboloidonesheet_orthographic",
        folder="hyperboloidonesheet",
    )

    renderer_orthographic.render()
    renderer_orthographic.save(format="png")


def demo_hyperboloidtwosheets():
    print("Démo : Hyperboloïde à deux nappes (Perspective vs Orthographique)")

    H2 = HyperboloidTwoSheets(color=(240, 47, 79), apply_grid_pattern=True)
    world = P2 + H2
    # ==========================================
    # PERSPECTIVE
    # ==========================================

    scene_perspective = Scene(perspective_camera, world)

    renderer_persp = Renderer(
        scene_perspective,
        name="hyperboloidtwosheets_perspective",
        folder="hyperboloidtwosheets",
    )

    renderer_persp.render()
    renderer_persp.save(format="png")

    # ==========================================
    # ORTHOGRAPHIC
    # ==========================================

    H2.apply_grid_pattern = False

    scene_orthographic = Scene(orthographic_camera, world)

    renderer_orthographic = Renderer(
        scene_orthographic,
        name="hyperboloidtwosheets_orthographic",
        folder="hyperboloidtwosheets",
    )

    renderer_orthographic.render()
    renderer_orthographic.save(format="png")


def demo_roman():
    print("Démo : Surface de Roman (Perspective vs Orthographique)")

    R = Roman(color=(240, 47, 79), apply_grid_pattern=True)
    world = P2 + R
    # ==========================================
    # PERSPECTIVE
    # ==========================================

    scene_perspective = Scene(perspective_camera, world)

    renderer_persp = Renderer(
        scene_perspective,
        name="roman_perspective",
        folder="roman",
    )

    renderer_persp.render()
    renderer_persp.save(format="png")

    # ==========================================
    # ORTHOGRAPHIC
    # ==========================================

    R.apply_grid_pattern = False

    scene_orthographic = Scene(orthographic_camera, world)

    renderer_orthographic = Renderer(
        scene_orthographic,
        name="roman_orthographic",
        folder="roman",
    )

    renderer_orthographic.render()
    renderer_orthographic.save(format="png")


def demo_caylay():
    print("Démo : Surface de Caylay (Perspective vs Orthographique)")

    C = Caylay(color=(240, 47, 79), apply_grid_pattern=True).scale(0.4, 0.4, 0.4)
    world = P2 + C
    # ==========================================
    # PERSPECTIVE
    # ==========================================

    scene_perspective = Scene(perspective_camera, world)

    renderer_persp = Renderer(
        scene_perspective,
        name="caylay_perspective",
        folder="caylay",
    )

    renderer_persp.render()
    renderer_persp.save(format="png")

    # ==========================================
    # ORTHOGRAPHIC
    # ==========================================

    C.apply_grid_pattern = False

    scene_orthographic = Scene(orthographic_camera, world)

    renderer_orthographic = Renderer(
        scene_orthographic,
        name="caylay_orthographic",
        folder="caylay",
    )

    renderer_orthographic.render()
    renderer_orthographic.save(format="png")


def demo_steiner2():
    print("Démo : Surface de Steiner2 (Perspective vs Orthographique)")

    S2 = Steiner2(color=(240, 47, 79), apply_grid_pattern=True)
    world = P2 + S2
    # ==========================================
    # PERSPECTIVE
    # ==========================================

    scene_perspective = Scene(perspective_camera, world)

    renderer_persp = Renderer(
        scene_perspective,
        name="steiner2_perspective",
        folder="steiner2",
    )

    renderer_persp.render()
    renderer_persp.save(format="png")

    # ==========================================
    # ORTHOGRAPHIC
    # ==========================================

    S2.apply_grid_pattern = False

    scene_orthographic = Scene(orthographic_camera, world)

    renderer_orthographic = Renderer(
        scene_orthographic,
        name="steiner2_orthographic",
        folder="steiner2",
    )

    renderer_orthographic.render()
    renderer_orthographic.save(format="png")


def demo_steiner4():
    print("Démo : Surface de Steiner4 (Perspective vs Orthographique)")

    S4 = Steiner4(color=(240, 47, 79), apply_grid_pattern=True).rotate_z(DEG * 30)
    world = P2 + S4
    # ==========================================
    # PERSPECTIVE
    # ==========================================

    scene_perspective = Scene(perspective_camera, world)

    renderer_persp = Renderer(
        scene_perspective,
        name="steiner4_perspective",
        folder="steiner4",
    )

    renderer_persp.render()
    renderer_persp.save(format="png")

    # ==========================================
    # ORTHOGRAPHIC
    # ==========================================

    S4.apply_grid_pattern = False

    scene_orthographic = Scene(orthographic_camera, world)

    renderer_orthographic = Renderer(
        scene_orthographic,
        name="steiner4_orthographic",
        folder="steiner4",
    )

    renderer_orthographic.render()
    renderer_orthographic.save(format="png")


def demo_whitney_umbrella():
    print("Démo : Paraplui de Witney (Perspective vs Orthographique)")

    W = WhitneyUmbrella(color=(240, 47, 79), apply_grid_pattern=True)
    world = P2 + W
    # ==========================================
    # PERSPECTIVE
    # ==========================================

    scene_perspective = Scene(perspective_camera, world)

    renderer_persp = Renderer(
        scene_perspective,
        name="witney_umbrella_perspective",
        folder="witney_umbrella",
    )

    renderer_persp.render()
    renderer_persp.save(format="png")

    # ==========================================
    # ORTHOGRAPHIC
    # ==========================================

    W.apply_grid_pattern = False

    scene_orthographic = Scene(orthographic_camera, world)

    renderer_orthographic = Renderer(
        scene_orthographic,
        name="witney_umbrella_orthographic",
        folder="witney_umbrella",
    )

    renderer_orthographic.render()
    renderer_orthographic.save(format="png")


def demo_csg_0():
    S = Sphere(1, color=(240, 47, 79), apply_grid_pattern=True)
    R = Roman(color=(240, 47, 79), apply_grid_pattern=True)

    objet_csg_0 = R - S.scale(0.7, 0.7, 0.7)

    world = P2 + objet_csg_0

    scene_persp = Scene(perspective_camera, world)
    renderer_persp = Renderer(scene_persp, name="csg_0", folder="csg")

    renderer_persp.render()
    renderer_persp.save(format="png")

    return Scene(perspective_camera, world)


def demo_csg_1():
    H1 = HyperboloidOneSheet(color=(240, 47, 79), apply_grid_pattern=True)
    T = Tore(0.2, 0.8, color=(240, 47, 79), apply_grid_pattern=True)

    objet_csg_1 = H1 & T.scale(1.25, 1.25, 1.25)

    world = P2 + objet_csg_1

    scene_persp = Scene(perspective_camera, world)
    renderer_persp = Renderer(scene_persp, name="csg_1", folder="csg")

    renderer_persp.render()
    renderer_persp.save(format="png")

    return Scene(perspective_camera, P2 + objet_csg_1)


def demo_csg_2():
    S = Sphere(1, color=(240, 47, 79), apply_grid_pattern=True)
    C = Caylay(color=(240, 47, 79), apply_grid_pattern=True).scale(0.4, 0.4, 0.4)
    C2 = (
        Caylay(color=(240, 47, 79), apply_grid_pattern=True)
        .scale(0.4, 0.4, 0.4)
        .rotate_z(90 * DEG)
    )
    objet_csg_2 = (C + C2) & S

    world = P2 + objet_csg_2

    scene_persp = Scene(perspective_camera, world)
    renderer_persp = Renderer(scene_persp, name="csg_2", folder="csg")

    renderer_persp.render()
    renderer_persp.save(format="png")

    return Scene(perspective_camera, P2 + objet_csg_2)


def demo_lens_perspective():
    S_gauche = Sphere(1.0, color=(100, 200, 255), apply_grid_pattern=True).translate(
        -0.6, 0, 0
    )
    S_droite = Sphere(1.0, color=(100, 200, 255), apply_grid_pattern=True).translate(
        0.6, 0, 0
    )

    lens = S_gauche & S_droite

    world = P2 + lens

    scene_persp = Scene(perspective_camera, world)
    renderer_persp = Renderer(scene_persp, name="lens", folder="csg")

    renderer_persp.render()
    renderer_persp.save(format="png")

    return Scene(perspective_camera, P2 + lens)


def demo_barillet_anim():
    cyl_infini = Cylindre(0.55, color=(240, 47, 79), apply_grid_pattern=False)
    perspective_camera.light_dir = normalize3((1, -1, 1))
    # La sphère qui va "boucher" le haut et le bas (Intersection)
    boite_coupe = Sphere(0.75, color=(240, 47, 79))

    barillet_base = cyl_infini & boite_coupe

    trou_central = Cylindre(0.1, color=(240, 47, 79), apply_grid_pattern=False)

    r_chambre = 0.15
    d = 0.33  # Distance entre le centre du barillet et le centre d'une chambre

    t0 = Cylindre(r_chambre, color=(240, 47, 79), apply_grid_pattern=False).translate(
        d, 0, 0
    )
    t1 = (
        Cylindre(r_chambre, color=(240, 47, 79), apply_grid_pattern=False)
        .translate(d, 0, 0)
        .rotate_z(60 * DEG)
    )
    t2 = (
        Cylindre(r_chambre, color=(240, 47, 79), apply_grid_pattern=False)
        .translate(d, 0, 0)
        .rotate_z(120 * DEG)
    )
    t3 = (
        Cylindre(r_chambre, color=(240, 47, 79), apply_grid_pattern=False)
        .translate(d, 0, 0)
        .rotate_z(180 * DEG)
    )
    t4 = (
        Cylindre(r_chambre, color=(240, 47, 79), apply_grid_pattern=False)
        .translate(d, 0, 0)
        .rotate_z(240 * DEG)
    )
    t5 = (
        Cylindre(r_chambre, color=(240, 47, 79), apply_grid_pattern=False)
        .translate(d, 0, 0)
        .rotate_z(300 * DEG)
    )

    barillet = barillet_base - trou_central - t0 - t1 - t2 - t3 - t4 - t5

    barillet.rotate_x(45 * DEG).rotate_y(30 * DEG)
    sol = Plane(color=white, apply_grid_pattern=False).translate(0, 0, -1.5)

    world = sol + barillet
    scene_perspective = Scene(perspective_camera, sol + barillet)

    renderer_persp = Renderer(
        scene_perspective,
        name="barillet_anim",
        folder="barillet_anim",
    )

    for _ in range(90):
        barillet.rotate_z(DEG * 4)
        renderer_persp.render()
    renderer_persp.save(format="gif")


def demo_solar_system_perspective():

    soleil = Sphere(0.5, color=(255, 200, 0), apply_grid_pattern=False)

    planete = Sphere(0.2, color=(100, 100, 255), apply_grid_pattern=False)
    planete.translate(2.0, 0.0, 0.0)

    world = soleil + planete

    scene_persp = Scene(perspective_camera, world)
    renderer_persp = Renderer(scene_persp, name="sphere_perspective", folder="sphere")

    renderer_persp.render()
    renderer_persp.save(format="png")

    return Scene(soleil + planete)


def creer_cube_csg(color=(50, 150, 255), apply_grid_pattern=True):
    # --- 1. L'axe Z (Haut et Bas) ---
    # Le plafond (garde tout ce qui est en dessous de z = 0.5)
    H_z_pos = HalfSpace(color, apply_grid_pattern=apply_grid_pattern).translate(
        0, 0, 0.5
    )
    # Le plancher (tourné de 180° pour pointer vers le bas, repoussé à z = -0.5)
    H_z_neg = (
        HalfSpace(color, apply_grid_pattern=apply_grid_pattern)
        .rotate_x(180 * DEG)
        .translate(0, 0, -0.5)
    )

    # --- 2. L'axe X (Droite et Gauche) ---
    # Face droite (tournée de 90° sur Y pour pointer vers +X, repoussée à x = 0.5)
    H_x_pos = (
        HalfSpace(color, apply_grid_pattern=apply_grid_pattern)
        .rotate_y(90 * DEG)
        .translate(0.5, 0, 0)
    )
    # Face gauche (tournée de -90° sur Y pour pointer vers -X, repoussée à x = -0.5)
    H_x_neg = (
        HalfSpace(color, apply_grid_pattern=apply_grid_pattern)
        .rotate_y(-90 * DEG)
        .translate(-0.5, 0, 0)
    )

    # --- 3. L'axe Y (Avant et Arrière) ---
    # Face avant (tournée de -90° sur X pour pointer vers +Y, repoussée à y = 0.5)
    H_y_pos = (
        HalfSpace(color, apply_grid_pattern=apply_grid_pattern)
        .rotate_x(-90 * DEG)
        .translate(0, 0.5, 0)
    )
    # Face arrière (tournée de +90° sur X pour pointer vers -Y, repoussée à y = -0.5)
    H_y_neg = (
        HalfSpace(color, apply_grid_pattern=apply_grid_pattern)
        .rotate_x(90 * DEG)
        .translate(0, -0.5, 0)
    )

    # L'intersection de ces 6 demi-espaces infinis crée un cube fini !
    return H_z_pos & H_z_neg & H_x_pos & H_x_neg & H_y_pos & H_y_neg


def demo_cube_csg():
    print("🎬 Démo : Le Cube CSG (Intersection de 6 HalfSpaces)")

    # On crée notre cube et on l'incline pour le style
    mon_cube = creer_cube_csg(color=(240, 47, 79), apply_grid_pattern=False)
    # mon_cube.rotate_x(45 * DEG).rotate_z(35 * DEG)

    # On le pose sur un sol
    sol = Plane(color=(200, 200, 200), apply_grid_pattern=False).translate(0, 0, -1.5)
    monde = sol + mon_cube

    perspective_camera.cam_o = (0, -3, 0)
    perspective_camera.light_dir = normalize3((1.0, -1.5, 1.0))

    scene = Scene(orthographic_camera, monde)
    renderer = Renderer(scene, name="cube_csg", folder="primitives")

    renderer.render()
    renderer.save(format="png")
