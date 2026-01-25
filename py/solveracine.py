from bernstein import *
from Casteljau import *
from Polynome import *


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
            solutions_apres_gauche = solve(epsilon, tab1, t1, tm, solutions)
            return solve(epsilon, tab2, tm, t2, solutions_apres_gauche)


def racine(tab):

    epsilon = 1e-5

    roots = solve(epsilon, tobernstein(tab[::-1]), 0, 1.0, [])

    return [1.0 / x for x in reversed(roots)]
