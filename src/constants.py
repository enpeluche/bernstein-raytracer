# --- Mathématiques ---
PI = 3.1415926535
DEG = PI / 180.0

# --- Paramètres de Rendu ---
FOG_START = 10.0
FOG_END = 15

SHADOW_BIAS = 0.001
SHADOW_OPACITY = 0.3
AMBIENT_LIGHT = 0.12

RENDER_SIZE = 1000

# --- Palette de Couleurs (RGB) ---
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)


UP = (0.0, 0.0, 1.0)


EPSILON = 1e-9


RAY_PROTOCOL = ["ox", "oy", "oz", "dx", "dy", "dz", "O2", "D2", "OD"]
NORMAL_PROTOCOL = ["x", "y", "z"]


GRID_SPACING = 0.25

GRID_THICKNESS_SCALE = 0.0008

GRID_BASE_THICKNESS = 0.003

GRID_MAX_THICKNESS = GRID_SPACING * 0.4
