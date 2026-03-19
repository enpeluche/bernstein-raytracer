from .camera import (
    PerspectiveCamera,
    OrthographicCamera,
    FOVPerspectiveCamera,
    FisheyeCamera,
    ThinLensCamera,
    CylindricalCamera,
)

camera_0 = PerspectiveCamera(
    origin=(3, -5, 3),
    view_direction=(-3, 5, -3),
    light_dir=(1, -2, 0.75),
    name="perspectivecamera",
    focale=1.5,
)

camera_1 = OrthographicCamera(
    origin=(0.0, -3.0, 0.0),
    view_direction=(0.0, 1.0, 0.0),
    light_dir=(1, -2, 0.75),
    size_world=2.0,
    name="orthographiccamera",
)


camera_2 = FOVPerspectiveCamera(
    origin=(1.0, -2.0, 0.0),
    view_direction=(-1.0, 2.0, 0.0),
    light_dir=(1.0, -2.0, 0.75),
    name="fovperspectivecamera",
    fov_deg=60.0,
)


camera_3 = FisheyeCamera(
    origin=(0.0, -1.5, -0.2),
    view_direction=(0.0, 1.5, 0.2),
    light_dir=(1.0, -2.0, 0.75),
    name="fisheyecamera",
    fov_deg=90.0,
)


camera_4 = ThinLensCamera(
    origin=(0.0, -3.0, 0.0),
    view_direction=(0.0, 1.0, 0.0),
    light_dir=(1.0, -2.0, 0.75),
    name="thinLenscamera",
    fov_deg=60.0,
    aperture=0.15,
    focus_dist=3.0,
)


camera_5 = CylindricalCamera(
    origin=(0.0, -3.0, 0.0),
    view_direction=(0.0, 1.0, 0.0),
    light_dir=(1.0, -2.0, 0.75),
    name="cylindricalcamera",
    fov_deg=180.0,
)

camera_6 = OrthographicCamera(
    origin=(5.0, -5.0, 5.0),  # Placée en hauteur et en diagonale
    view_direction=(-5.0, 5.0, -5.0),  # Regarde vers l'origine (0,0,0)
    light_dir=(1.0, -2.0, 0.75),
    size_world=3.0,
    name="isometric_orthographic",
)

camera_7 = ThinLensCamera(
    origin=(0.5, -1.0, 0.5),
    view_direction=(-0.5, 1.0, -0.5),
    light_dir=(1.0, -2.0, 0.75),
    name="macro_camera",
    fov_deg=45.0,
    aperture=0.8,  # Ouverture massive pour un flou (bokeh) prononcé
    focus_dist=1.22,  # Mise au point millimétrée
)
cameras = [
    camera_0,
    camera_1,
    camera_2,
    camera_3,
    camera_4,
    camera_5,
    camera_6,
    camera_7,
]
