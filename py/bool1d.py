from Intervalle import Intervalle


def union(A, B):  # A est une liste d'Intervalle

    if A == []:
        return B

    if B == []:
        return A

    [a1, a2] = [A[0].a.t, A[0].b.t]
    [b1, b2] = [B[0].a.t, B[0].b.t]

    assert a1 <= a2
    assert b1 <= b2

    if a1 > b1:
        return union(B, A)

    assert a1 <= b1

    # cas disjoint
    if a2 < b1:

        return [A[0]] + union(A[1:], B)

    assert a2 >= b1

    # si [b1, b2] est inclu dans [a1, a2]
    if b2 <= a2:
        return union(A, B[1:])

    assert b2 > a2

    return union([Intervalle(A[0].a, B[0].b)] + A[1:], B[1:])


def inter_iterative(A, B):
    result = []
    i, j = 0, 0

    len_a = len(A)
    len_b = len(B)

    while i < len_a and j < len_b:
        # On récupère les deux intervalles courants
        ia = A[i]
        ib = B[j]

        # --- 1. CALCUL DES BORNES DE L'INTERSECTION ---
        # Le début de l'intersection est le plus TARDIF des deux débuts
        # La fin de l'intersection est le plus TÔT des deux fins

        # Choix du Hit de départ
        if ia.a.t > ib.a.t:
            start_hit = ia.a
            t_start = ia.a.t
        else:
            start_hit = ib.a
            t_start = ib.a.t

        # Choix du Hit de fin
        if ia.b.t < ib.b.t:
            end_hit = ia.b
            t_end = ia.b.t
        else:
            end_hit = ib.b
            t_end = ib.b.t

        # --- 2. VALIDATION ---
        # Si le début est avant la fin, l'intersection existe
        if t_start < t_end:
            # On crée un NOUVEL intervalle avec les bons Hits
            result.append(Intervalle(start_hit, end_hit))

        # --- 3. AVANCEMENT (Qui finit le premier ?) ---
        # L'intervalle qui se termine le plus tôt est "épuisé", on passe au suivant.
        if ia.b.t < ib.b.t:
            i += 1
        else:
            j += 1

    return result


def inter(A, B):
    if A == [] or B == []:
        return []

    [a1, a2] = [A[0].a.t, A[0].b.t]
    [b1, b2] = [B[0].a.t, B[0].b.t]

    assert a1 <= a2
    assert b1 <= b2

    if a1 > b1:
        return inter(B, A)

    assert a1 <= b1

    if a2 < b1:  # disjoints
        return inter(A[1:], B)

    assert a2 >= b1

    if b2 <= a2:  # ya une inclusion
        return [B[0]] + inter(A, B[1:])

    else:
        return [Intervalle(B[0].a, A[0].b)] + inter(A[1:], B)


def differ(A, B):
    if A == []:
        return []

    if not B:
        return A

    else:
        [a1, a2] = [A[0].a.t, A[0].b.t]
        [b1, b2] = [B[0].a.t, B[0].b.t]

        assert a1 <= a2
        assert b1 <= b2

        if b2 <= a1:
            return differ(A, B[1:])

        elif a2 <= b1:
            return [A[0]] + differ(A[1:], B)

        elif b1 <= a1:
            if b2 <= a2:
                return differ([Intervalle(B[0].b, A[0].b)] + A[1:], B[1:])

            else:
                return differ(A[1:], B)

        elif a2 <= b2:
            return [Intervalle(A[0].a, B[0].a)] + differ(A[1:], B)

        else:
            return [Intervalle(A[0].a, B[0].a)] + differ(
                [Intervalle(B[0].b, A[0].b)] + A[1:], B[1:]
            )


def union1D_iterative(A, B):
    # --- PARTIE 1 : MERGE (Tri) ---
    # (Cette partie est juste, je la garde telle quelle)
    merged_list = []
    i, j = 0, 0
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

    # --- PARTIE 2 : SWEEP (Fusion) ---

    # On initialise avec une COPIE du premier pour ne pas casser les listes originales
    # (Supposons que tu as une méthode copy() ou que tu crées un nouvel Intervalle)
    result = [merged_list[0]]

    for current in merged_list[1:]:
        last = result[-1]

        # 1. CAS CHEVAUCHEMENT (Overlap)
        if current.a.t <= last.b.t:
            # On ne fait rien si current est entièrement inclus (cas [0,10] et [2,5])
            # On agit SEULEMENT si current dépasse la fin de last (cas [0,5] et [4,8])
            if current.b.t > last.b.t:
                # FUSION : On étend la fin de l'intervalle existant
                # On remplace le 'b' (sortie) de last par celui de current
                last.b = current.b
                # (Ici on modifie l'objet 'last' qui est DÉJÀ dans 'result')

        # 2. CAS DISJOINT (Trou entre les deux)
        else:
            # On ajoute le nouvel intervalle à la suite
            result.append(current)

    return result


def union1D(A, B):
    print("union1D")

    print(f"A:{A}")
    print(f"B:{B}")

    if A == []:
        return B

    if B == []:
        return A

    [a1, a2] = A[0]
    [b1, b2] = B[0]

    assert a1 <= a2
    assert b1 <= b2

    if a1 > b1:
        return union1D(B, A)

    assert a1 <= b1

    # cas disjoint
    if a2 < b1:
        return [[a1, a2]] + union1D(A[1:], B)

    assert a2 >= b1

    # si [b1, b2] est inclu dans [a1, a2]
    if b2 <= a2:
        return union1D(A, B[1:])

    assert b2 > a2

    return union1D([[a1, b2]] + A[1:], B[1:])


def inter1D(A, B):
    print("inter1D")

    print(f"A:{A}")
    print(f"B:{B}")

    if A == [] or B == []:
        return []

    [a1, a2] = A[0]
    [b1, b2] = B[0]

    assert a1 <= a2
    assert b1 <= b2

    if a1 > b1:
        return inter1D(B, A)

    assert a1 <= b1

    if a2 < b1:  # disjoints
        return inter1D(A[1:], B)

    assert a2 >= b1

    if b2 <= a2:  # ya une inclusion
        return [[b1, b2]] + inter1D(A, B[1:])

    else:
        return [[b1, a2]] + inter1D(A[1:], B)


if __name__ == "__main__":
    A = [[0, 5], [6, 7]]
    B = [[4, 8]]

    print(f"\n Résultat: {union1D(A, B)}")
