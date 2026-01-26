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

    # On inverse les coefficients pour transformer x en 1/x
    # Les racines 'u' trouvées ici dans [0, 1] correspondent à t = 1/u dans [1, inf]
    roots_far_inv = solve(epsilon, tobernstein(tab[::-1]), 0, 1.0, [])

    # On convertit u -> 1/u
    roots_far = []
    for u in roots_far_inv:
        if abs(u) > epsilon:
            t = 1.0 / u
            # si t=1, on l'a peut-être déjà trouvé dans la passe 1
            if t > 1.0 + epsilon:
                roots_far.append(t)
        # else:
        #    print(f"racine: abs(u):{abs(u)} <= epsilon:{epsilon}")

    # On remet dans l'ordre (les racines lointaines sont souvent trouvées dans le désordre par l'inverse)
    solutions.extend(sorted(roots_far))

    return solutions
