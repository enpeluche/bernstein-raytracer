from constants import *
from Shapes import *
from Cameras import *
from Object import *
from Scene import *
from Renderer import *


camera = CameraPerspective(
    cam_o=(0.0, -3, 0.0),
    cam_dx=(1.0, 0.0, 0.0),
    cam_dy=(0.0, 1.0, 0.0),  # la direction des rayons aussi
    cam_dz=(0.0, 0.0, 1.0),
    size_world=2,
    size_win=500,
    light_dir=(0, -1, 1),
    name="",
    focale=1.0,
)

P = Plane(color=(58, 157, 35))
H1 = HyperboloidOneSheet()
H2 = HyperboloidTwoSheets()
R = Roman()
S = Sphere(1)
T = Tore(0.2, 1)
C = Caylay()
S2 = Steiner2()
S4 = Steiner4()

P.translate(0, 0, -1)
W = WhitneyUmbrella(color=(133, 87, 200))
scene = Scene(camera, W)
renderer = Renderer(scene)

for _ in range(180):
    W.rotate_z(DEG).rotate_y(DEG).rotate_z(DEG)
    renderer.render()
renderer.save(format="gif")
