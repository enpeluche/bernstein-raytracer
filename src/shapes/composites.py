from .quadrics import sphere
from .linear import HalfSpace
from ..constants import DEG


def cube(color=None, show_grid=False):
    """
    A solid cube defined by the intersection of 6 Half-spaces.
    Often referred to as a Box or AABB in graphics engines.
    """

    H_z_pos = HalfSpace(color=color, show_grid=show_grid).translate(0, 0, 0.5)
    H_z_neg = (
        HalfSpace(color=color, show_grid=show_grid)
        .rotate_x(180 * DEG)
        .translate(0, 0, -0.5)
    )

    H_x_pos = (
        HalfSpace(color=color, show_grid=show_grid)
        .rotate_y(90 * DEG)
        .translate(0.5, 0, 0)
    )

    H_x_neg = (
        HalfSpace(color=color, show_grid=show_grid)
        .rotate_y(-90 * DEG)
        .translate(-0.5, 0, 0)
    )

    H_y_pos = (
        HalfSpace(color=color, show_grid=show_grid)
        .rotate_x(-90 * DEG)
        .translate(0, 0.5, 0)
    )

    H_y_neg = (
        HalfSpace(color=color, show_grid=show_grid)
        .rotate_x(90 * DEG)
        .translate(0, -0.5, 0)
    )

    return H_z_pos & H_z_neg & H_x_pos & H_x_neg & H_y_pos & H_y_neg


def lens(R: float, h: float, color=None):
    s1 = sphere(radius=R, color=color).translate(-h, 0.0, 0.0)
    s2 = sphere(radius=R, color=color).translate(h, 0.0, 0.0)

    return s1 & s2
