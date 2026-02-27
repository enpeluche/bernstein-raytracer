from Intervalle import Intervalle


def union1D_iterative(A, B):
    """
    Fusionne deux listes d'intervalles (Union CSG) de manière itérative.

    Args:
        A (list[Intervalle]): La première liste d'intervalles (triée par t).
        B (list[Intervalle]): La deuxième liste d'intervalles (triée par t).

    Returns:
        list[Intervalle]: La liste résultante des intervalles fusionnés.
    """

    merged_list = []

    i, j = 0, 0

    # Étape 1 : Tri fusion des deux listes
    while i < len(A) and j < len(B):
        if A[i].a.t < B[j].a.t:
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

        if current.a.t <= last.b.t:
            # Chevauchement ou inclusion : on étend la borne supérieure si nécessaire
            if current.b.t > last.b.t:
                last.b = current.b

        else:
            # Disjoint : on ajoute le nouvel intervalle
            result.append(current)

    return result


def inter_iterative(A, B):
    """
    Calcule l'intersection de deux listes d'intervalles de manière itérative.

    Args:
        A (list[Intervalle]): La première liste d'intervalles.
        B (list[Intervalle]): La deuxième liste d'intervalles.

    Returns:
        list[Intervalle]: La liste résultante de l'intersection.
    """
    result = []
    i, j = 0, 0

    len_a = len(A)
    len_b = len(B)

    while i < len_a and j < len_b:
        ia = A[i]
        ib = B[j]

        # Choix du Hit de début (le plus tardif des deux)
        if ia.a.t > ib.a.t:
            start_hit = ia.a
            t_start = ia.a.t
        else:
            start_hit = ib.a
            t_start = ib.a.t

        # Choix du Hit de fin (le plus précoce des deux)
        if ia.b.t < ib.b.t:
            end_hit = ia.b
            t_end = ia.b.t
        else:
            end_hit = ib.b
            t_end = ib.b.t

        # Si l'intervalle est valide, on l'ajoute
        if t_start < t_end:
            result.append(Intervalle(start_hit, end_hit))

        # Avancement : l'intervalle qui se termine le plus tôt est épuisé
        if ia.b.t < ib.b.t:
            i += 1
        else:
            j += 1

    return result


def differ(A, B):
    """
    Calcule la différence entre deux listes d'intervalles (A - B) de manière récursive.

    Args:
        A (list[Intervalle]): La liste d'intervalles de l'objet principal.
        B (list[Intervalle]): La liste d'intervalles de l'objet à soustraire.

    Returns:
        list[Intervalle]: La liste résultante de la soustraction.
    """

    if A == []:
        return []

    if not B:
        return A

    else:
        # Déballage rapide sans créer de listes inutiles
        a1, a2 = [A[0].a.t, A[0].b.t]
        b1, b2 = [B[0].a.t, B[0].b.t]

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
                return differ([Intervalle(B[0].b, A[0].b)] + A[1:], B[1:])

            else:
                return differ(A[1:], B)

        elif a2 <= b2:
            # B ampute la fin de A
            return [Intervalle(A[0].a, B[0].a)] + differ(A[1:], B)

        else:
            # B coupe A en plein milieu (création d'un trou)
            return [Intervalle(A[0].a, B[0].a)] + differ(
                [Intervalle(B[0].b, A[0].b)] + A[1:], B[1:]
            )
