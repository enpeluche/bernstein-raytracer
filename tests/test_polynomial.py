from src.Polynomial import Polynomial

import random
from src.constants import EPSILON

DEG = 100


def test_is_root():
    for _ in range(1000):
        P = Polynomial([random.random() for _ in range(DEG)])
        roots = P.roots()

        for root in roots:
            value = P(root)

            assert abs(value) < EPSILON, (
                f"P={P.coefficients}, "
                f"Manque de précision ! Pour t={root}, "
                f"P(t) devrait valoir 0, mais vaut {value}"
            )


def test_racines_connues():
    """Construit un polynôme à partir de racines connues et vérifie qu'on les retrouve."""

    # 1. On choisit des racines distinctes et bien espacées dans ]0, 1[
    racines_attendues = [0.15, 0.45, 0.75]

    # 2. Construction des coefficients (développement de (t - r1)(t - r2)...)
    # On part d'un polynôme P(t) = 1 (coeff canonique constant)
    coeffs = [1.0]
    for r in racines_attendues:
        # On multiplie le polynôme courant par (t - r)
        # (t - r) se traduit par les coefficients [-r, 1]
        nouveaux_coeffs = [0.0] * (len(coeffs) + 1)
        for i, c in enumerate(coeffs):
            nouveaux_coeffs[i] -= c * r  # La partie constante (-r)
            nouveaux_coeffs[i + 1] += c  # La partie en t (+1)
        coeffs = nouveaux_coeffs

    # 3. On crée le polynôme avec ces coefficients générés
    P = Polynomial(coeffs)
    racines_trouvees = P.roots()  # Ou P.roots(0, 1) selon comment tu l'as codé

    # 4. Les vérifications
    assert len(racines_trouvees) == len(
        racines_attendues
    ), f"Le solveur a trouvé {len(racines_trouvees)} racines au lieu de {len(racines_attendues)} : {racines_trouvees}"

    # On trie les deux listes pour comparer la plus petite avec la plus petite, etc.
    racines_trouvees.sort()
    racines_attendues.sort()

    for rt, ra in zip(racines_trouvees, racines_attendues):
        assert abs(rt - ra) < 1e-6, f"Décalage ! Racine trouvée: {rt}, attendue: {ra}"


def test_invariant_degre_racines():
    """Vérifie qu'un polynôme n'a jamais plus de racines que son degré."""
    for _ in range(1000):
        # On génère un degré aléatoire entre 1 et 20
        degre = random.randint(1, 100)
        coeffs = [random.uniform(-10, 10) for _ in range(degre + 1)]

        P = Polynomial(coeffs)
        racines = P.roots()

        # L'invariant : nb_racines <= degre
        assert len(racines) <= degre, (
            f"Anomalie mathématique ! Degré {degre} mais {len(racines)} racines trouvées. "
            f"Coeffs: {coeffs}"
        )


def test_polynome_nul():
    """Vérifie qu'un polynôme dont tous les coefficients sont nuls ne fait pas planter le solveur."""
    P = Polynomial([0.0] * 10)
    # Selon ta logique, soit il renvoie [], soit il renvoie les bornes.
    # L'important est qu'il ne crash pas.
    roots = P.roots()
    assert isinstance(roots, list)


def test_racine_double():
    """Un polynôme qui frôle l'axe (ex: (t-0.5)^2) doit être géré proprement."""
    # Coeffs de t^2 - t + 0.25
    P = Polynomial([0.25, -1.0, 1.0])
    roots = P.roots()
    # On veut vérifier qu'on trouve au moins une racine proche de 0.5
    assert any(abs(r - 0.5) < 1e-3 for r in roots)


def test_degre_effectif():
    P = Polynomial([0, 0, 1])  # en fait degré 2

    roots = P.roots()
    assert len(roots) <= 2


def test_racine_double():
    """Un polynôme qui frôle l'axe (ex: (t-0.5)^2) doit être géré proprement."""
    # Coeffs de t^2 - t + 0.25
    P = Polynomial([0.25, -1.0, 1.0])
    roots = P.roots()
    # On veut vérifier qu'on trouve au moins une racine proche de 0.5
    assert any(abs(r - 0.5) < 1e-3 for r in roots)


def test_coherence_signe():
    P = Polynomial([-0.12, 1.0, -1.0])  # exemple simple

    roots = sorted(P.roots())

    points = [0.0] + roots + [1.0]

    for i in range(len(points) - 1):
        mid = 0.5 * (points[i] + points[i + 1])

        val = P(mid)

        # le signe ne doit pas osciller localement
        assert abs(val) > 1e-8


def test_completude():
    racines = [0.2, 0.2, 0.5, 0.8, 0.8, 0.8]

    coeffs = [1.0]
    for r in racines:
        new = [0.0] * (len(coeffs) + 1)
        for i, c in enumerate(coeffs):
            new[i] -= c * r
            new[i + 1] += c
        coeffs = new

    P = Polynomial(coeffs)
    found = P.roots()

    # fusion géométrique
    def merge(xs, eps=1e-5):
        xs = sorted(xs)
        out = []
        for x in xs:
            if not out or abs(x - out[-1]) > eps:
                out.append(x)
        return out

    assert len(merge(found)) == 3


def test_stabilite():
    base_roots = [0.2, 0.5, 0.8]

    # construire P
    coeffs = [1.0]
    for r in base_roots:
        new = [0.0] * (len(coeffs) + 1)
        for i, c in enumerate(coeffs):
            new[i] -= c * r
            new[i + 1] += c
        coeffs = new

    P = Polynomial(coeffs)
    roots1 = P.roots()

    # perturbation
    noisy = [c + random.uniform(-1e-8, 1e-8) for c in coeffs]
    P2 = Polynomial(noisy)
    roots2 = P2.roots()

    assert len(roots1) == len(roots2)


def test_racines_aux_bornes():
    """Vérifie qu'on trouve les racines situées pile sur 0.0 et 1.0."""
    # P(t) = t * (t - 1)  => Coeffs: [0, -1, 1]
    P = Polynomial([0.0, -1.0, 1.0])
    roots = P.roots()
    roots.sort()
    assert abs(roots[0] - 0.0) < 1e-7
    assert abs(roots[-1] - 1.0) < 1e-7
