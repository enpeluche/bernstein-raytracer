from Casteljau import Casteljau
from constants import EPSILON

# NOTE TECHNIQUE : Localisation vs Multiplicité
# Dans un contexte géométrique (intersection rayon-surface), seule la position
# topologique des racines est requise. La multiplicité algébrique n'est pas
# traitée ici : les racines multiples ou tangentes sont ramenées à une valeur
# unique. Cela optimise la stabilité numérique et répond au besoin du moteur
# de rendu (détection d'impact).


def solve(
    tab: list[float],
    t1: float,
    t2: float,
    v_min: float,
    v_max: float,
    solutions: list[float],
    depth: int = 0,
) -> list[float]:
    """
    Trouve les racines d'un polynôme défini par ses points de contrôle (base de Bernstein)
    en utilisant la subdivision récursive de De Casteljau.

    Args:
        tab (list[float]): Les points de contrôle du segment de courbe actuel.
        t1 (float): Borne paramétrique inférieure.
        t2 (float): Borne paramétrique supérieure.
        solutions (list[float]): Liste accumulant les racines trouvées (modifiée en place).
        depth (int, optional): Profondeur actuelle de la récursion. Défaut à 0.

    Returns:
        list[float]: La liste mise à jour des racines trouvées.
    """
    # Si le segment [t1, t2] est hors de la zone utile, on jette !
    if t2 < v_min or t1 > v_max:
        return solutions

    # 1. Sécurité : Limite de récursion (évite de bloquer sur les racines tangentes)
    if depth > 20:
        solutions.append((t1 + t2) * 0.5)
        return solutions

    # 2. Test de l'enveloppe convexe : la courbe traverse-t-elle le zéro ?
    if min(tab) > 0.0 or max(tab) < 0.0:
        return solutions

    # 3. Test de précision : l'intervalle est-il assez fin ?
    dt = t2 - t1

    if dt < EPSILON:
        solutions.append((t1 + t2) * 0.5)
        return solutions

    # 4. Subdivision : On coupe la courbe en deux moitiés
    tab1, tab2 = Casteljau(tab)

    tm = (t1 + t2) * 0.5

    solve(tab1, t1, tm, v_min, v_max, solutions, depth + 1)
    solve(tab2, tm, t2, v_min, v_max, solutions, depth + 1)

    return solutions


def has_root(
    tab: list[float],
    t1: float,
    t2: float,
    v_min: float,
    v_max: float,
    depth: int = 0,
) -> bool:
    """Variante ultra-rapide : s'arrête au premier signe de racine."""

    # 1. Hors limites ? On jette.
    if t2 < v_min or t1 > v_max:
        return False

    # 2. Racine trouvée par limite de profondeur ? BINGO.
    if depth > 20:
        return True

    # 3. Enveloppe convexe : pas de zéro croisé ? On jette.
    if min(tab) > 0.0 or max(tab) < 0.0:
        return False

    # 4. Racine trouvée par précision ? BINGO.
    dt = t2 - t1
    if dt < EPSILON:
        return True

    # 5. Subdivision
    tab1, tab2 = Casteljau(tab)
    tm = (t1 + t2) * 0.5

    # L'ARMEMENT DU SNIPER : Si la branche gauche trouve une racine,
    # Python ne calculera JAMAIS la branche droite (has_root(tab2...)).
    if has_root(tab1, t1, tm, v_min, v_max, depth + 1):
        return True

    return has_root(tab2, tm, t2, v_min, v_max, depth + 1)
