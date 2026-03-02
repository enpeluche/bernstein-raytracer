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

    solve(tab1, t1, tm, solutions, depth + 1)
    solve(tab2, tm, t2, solutions, depth + 1)

    return solutions
