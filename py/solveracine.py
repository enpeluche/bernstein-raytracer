from bernstein import *
from Casteljau import *


def solve(epsilon, tab, t1, t2, solutions):

    if 0.0 < min(tab) or 0.0 > max(tab):

        return solutions
    else:
        dt = t2 - t1

        if dt < epsilon:
            solutions.append((t1 + t2) * 0.5)
            return solutions

        else:
            (tab1, tab2) = Casteljau(tab)

            tm = (t1 + t2) * 0.5

            solve(epsilon, tab1, t1, tm, solutions)
            solve(epsilon, tab2, tm, t2, solutions)
            return solutions


def racine(tab):

    epsilon = 1e-6

    solutions = []

    roots_near = solve(epsilon, tobernstein(tab), 0, 1.0, [])
    solutions.extend(roots_near)

    roots_far_inv = solve(epsilon, tobernstein(tab[::-1]), 0, 1.0, [])

    roots_far = []
    for u in roots_far_inv:
        if abs(u) > epsilon:
            t = 1.0 / u

            if t > 1.0 + epsilon:
                roots_far.append(t)

    solutions.extend(sorted(roots_far))

    return solutions
