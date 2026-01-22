import math

def normalize3(v):

    (x, y, z) = v
    n = math.sqrt(x * x + y * y + z * z)
    if 0.0 == n:
        return (0.0, 0.0, 0.0)
    else:
        return (x / n, y / n, z / n)
    
def pscal3(x1, y1, z1, X):
    (x2, y2, z2) = X
    return x1 * x2 + y1 * y2 + z1 * z2

def clamp(mi, ma, v):
    return min(ma, max(mi, v))

def interpole(x1, y1, x2, y2, x):
    x1, y1, x2, y2, x = float(x1), float(y1), float(x2), float(y2), float(x)

    return ((x - x2) / (x1 - x2)) * y1 + ((x - x1) / (x2 - x1)) * y2