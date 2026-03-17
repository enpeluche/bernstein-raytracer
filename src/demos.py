from .constants import DEG, WHITE
from .camera import *
from .Scene import Scene
from .shapes import *
from .Renderer import *

camera_0 = PerspectiveCamera(
    origin=(0.0, -3, 0.0),
    view_direction=(0.0, 1.0, 0.0),
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
    origin=(0.0, -2.0, 0.0),
    view_direction=(0.0, 1.0, 0.0),
    light_dir=(1.0, -2.0, 0.75),
    name="fovperspectivecamera",
    fov_deg=60.0,
)


camera_3 = FisheyeCamera(
    origin=(0.0, -1.5, 0.0),
    view_direction=(0.0, 1.0, 0.0),
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

cameras = [camera_0, camera_1, camera_2, camera_3, camera_4, camera_5]


def render_camera_rig(obj, base_folder, cameras):
    """
    Renders a single primitive across the entire camera rig.
    Automatically organizes files by primitive label and camera name.
    """
    # Create a dedicated subfolder for this specific object
    object_folder = f"{base_folder}/{obj.label}"

    for cam in cameras:
        # Business Logic: Grid or no Grid?
        # Usually, we want the grid for everything EXCEPT Orthographic
        # to keep the "blueprint" look clean.
        obj.show_grid = "orthographic" not in cam.name

        # Construct a clean filename: e.g., "sphere_fisheyecamera"
        file_name = f"{obj.label}"

        print(f"    [Camera] {cam.name} -> {file_name}.png")

        # Core Rendering Pipeline
        scene = Scene(cam, obj)
        renderer = Renderer(scene, name=file_name, folder=object_folder)
        renderer.render()
        renderer.save(format="png")


def demo_full_suite(primitives, cameras, folder: str):
    print(f"🚀 Starting Multi-Camera Rig Suite ({len(cameras)} cameras configured)")

    for obj in primitives:
        print(f"\n--- Processing Primitive: {obj.label.upper()} ---")
        render_camera_rig(obj, f"gallery_suite/{folder}", cameras)

    print("✅ Rig rendering completed successfully.\n")
