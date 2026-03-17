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
