from Casteljau import *


def solve(epsilon, tab, t1, t2, solutions, depth=0):

    if depth > 20:
        solutions.append((t1 + t2) * 0.5)
        return solutions

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

            solve(epsilon, tab1, t1, tm, solutions, depth + 1)
            solve(epsilon, tab2, tm, t2, solutions, depth + 1)
            return solutions
