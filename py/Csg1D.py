from Interval import Interval


def union(A: list[Interval], B: list[Interval]) -> list[Interval]:
    """
    Fusionne deux listes d'intervalles (Union CSG) de manière itérative.

    Args:
        A (list[Interval]): La première liste d'intervalles (triée par t).
        B (list[Interval]): La deuxième liste d'intervalles (triée par t).

    Returns:
        list[Interval]: La liste résultante des intervalles fusionnés.
    """

    merged_list = []

    i, j = 0, 0

    # Étape 1 : Tri fusion des deux listes
    while i < len(A) and j < len(B):
        if A[i].hit_in.t < B[j].hit_in.t:
            merged_list.append(A[i])
            i += 1
        else:
            merged_list.append(B[j])
            j += 1

    merged_list.extend(A[i:])
    merged_list.extend(B[j:])

    if not merged_list:
        return []

    # Étape 2 : Fusion des intervalles qui se chevauchent
    result = [merged_list[0]]

    for current in merged_list[1:]:
        last = result[-1]

        if current.hit_in.t <= last.hit_out.t:
            # Chevauchement ou inclusion : on étend la borne supérieure si nécessaire
            if current.hit_out.t > last.hit_out.t:
                # avant : last.hit_out = current.hit_out
                result[-1] = Interval(last.hit_in, current.hit_out)

        else:
            # Disjoint : on ajoute le nouvel intervalle
            result.append(current)

    return result


def inter(A: list[Interval], B: list[Interval]) -> list[Interval]:
    """
    Calcule l'intersection de deux listes d'intervalles de manière itérative.

    Args:
        A (list[Interval]): La première liste d'intervalles.
        B (list[Interval]): La deuxième liste d'intervalles.

    Returns:
        list[Interval]: La liste résultante de l'intersection.
    """
    result = []
    i, j = 0, 0

    while i < len(A) and j < len(B):
        # Choix du hit_in (le plus tardif des deux)
        if A[i].hit_in.t > B[j].hit_in.t:
            start_hit = A[i].hit_in
            t_start = A[i].hit_in.t
        else:
            start_hit = B[j].hit_in
            t_start = B[j].hit_in.t

        # Choix du hit_out (le plus précoce des deux)
        if A[i].hit_out.t < B[j].hit_out.t:
            end_hit = A[i].hit_out
            t_end = A[i].hit_out.t
        else:
            end_hit = B[j].hit_out
            t_end = B[j].hit_out.t

        # Si l'intervalle est valide, on l'ajoute
        if t_start < t_end:
            result.append(Interval(start_hit, end_hit))

        # Avancement : l'intervalle qui se termine le plus tôt est épuisé
        if A[i].hit_out.t < B[j].hit_out.t:
            i += 1
        else:
            j += 1

    return result


def differ(A: list[Interval], B: list[Interval]) -> list[Interval]:
    """
    Calcule la différence entre deux listes d'intervalles A - B de manière récursive.

    Args:
        A (list[Interval]): La liste d'intervalles de l'objet principal.
        B (list[Interval]): La liste d'intervalles de l'objet à soustraire.

    Returns:
        list[Interval]: La liste résultante de la soustraction.
    """

    if A == []:
        return []

    if not B:
        return A

    else:
        # Déballage rapide sans créer de listes inutiles
        a1, a2 = [A[0].hit_in.t, A[0].hit_out.t]
        b1, b2 = [B[0].hit_in.t, B[0].hit_out.t]

        assert a1 <= a2
        assert b1 <= b2

        if b2 <= a1:
            # B est complètement avant A, on passe au B suivant
            return differ(A, B[1:])

        elif a2 <= b1:
            # B est complètement après A, le premier A est sauf
            return [A[0]] + differ(A[1:], B)

        elif b1 <= a1:
            # B couvre le début de A
            if b2 <= a2:
                return differ([Interval(B[0].hit_out, A[0].hit_out)] + A[1:], B[1:])

            else:
                return differ(A[1:], B)

        elif a2 <= b2:
            # B ampute la fin de A
            return [Interval(A[0].hit_in, B[0].hit_in)] + differ(A[1:], B)

        else:
            # B coupe A en plein milieu (création d'un trou)
            return [Interval(A[0].hit_in, B[0].hit_in)] + differ(
                [Interval(B[0].hit_out, A[0].hit_out)] + A[1:], B[1:]
            )
