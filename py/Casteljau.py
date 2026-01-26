def vecteurdesmilieux(v):
    l = len(v)
    vm = []

    for k in range(l - 1):
        vm.append((v[k] + v[k + 1]) * 0.5)
    return vm


def Casteljaujaujau(v):
    l = len(v)
    pv, dv, sv = [], [], []

    sv.append(v)

    for k in range(1, l):
        sv.append(vecteurdesmilieux(sv[k - 1]))

    for k in range(l):
        pv.append(sv[k][0])
        dv.append(sv[l - 1 - k][-1])

    return (pv, dv)


def Casteljau(v):
    n = len(v)

    # --- OPTIMISATION : Degré 2 (Sphères, Cylindres...)
    if n == 3:
        p0, p1, p2 = v
        # Étage 1
        m0 = (p0 + p1) * 0.5
        m1 = (p1 + p2) * 0.5
        # Sommet
        s = (m0 + m1) * 0.5
        # Retour immédiat
        return ([p0, m0, s], [s, m1, p2])

    # --- OPTIMISATION : Degré 3 (Bézier Cubique) ---
    if n == 4:
        p0, p1, p2, p3 = v
        # Étage 1
        m0 = (p0 + p1) * 0.5
        m1 = (p1 + p2) * 0.5
        m2 = (p2 + p3) * 0.5
        # Étage 2
        n0 = (m0 + m1) * 0.5
        n1 = (m1 + m2) * 0.5
        # Sommet
        s = (n0 + n1) * 0.5

        return ([p0, m0, n0, s], [s, n1, m2, p3])

    if n == 5:
        c0, c1, c2, c3, c4 = v

        # Étape 1
        m0 = (c0 + c1) * 0.5
        m1 = (c1 + c2) * 0.5
        m2 = (c2 + c3) * 0.5
        m3 = (c3 + c4) * 0.5

        # Étape 2
        m01 = (m0 + m1) * 0.5
        m12 = (m1 + m2) * 0.5
        m23 = (m2 + m3) * 0.5

        # Étape 3
        m012 = (m01 + m12) * 0.5
        m123 = (m12 + m23) * 0.5

        # Étape 4 (Point de scission)
        m0123 = (m012 + m123) * 0.5

        # Gauche : de c0 à m0123 / Droite : de m0123 à c4
        return ([c0, m0, m01, m012, m0123], [m0123, m123, m23, m3, c4])
    # 1. On crée une copie de travail 'temp' (taille N)
    # On évite de toucher à 'v' direct pour ne pas casser l'objet source
    temp = list(v)

    # 2. On initialise les résultats avec les extrêmes actuels
    pv = [temp[0]]  # Bord GAUCHE (P0)
    dv = [temp[-1]]  # Bord DROIT (Pn)

    # 3. Boucle principale (Réduction du triangle)
    # 'i' est l'étape (de 1 à n-1)
    for i in range(1, n):

        # Boucle interne : calcul des moyennes
        # On va jusqu'à n-i car la liste "utile" rétrécit à chaque étape
        for k in range(n - i):
            # CALCUL IN-PLACE : On écrase temp[k] avec la nouvelle valeur
            # C'est ici qu'on gagne du temps (pas de création de liste 'vm')
            temp[k] = (temp[k] + temp[k + 1]) * 0.5

        # À la fin de l'étape, on récupère les nouvelles extrémités
        pv.append(temp[0])  # Nouvelle pointe gauche
        dv.append(temp[n - 1 - i])  # Nouvelle pointe droite (le dernier calculé)

    # 4. On retourne (Gauche, Droite inversée)
    # dv est rempli à l'envers (du bas vers le haut du triangle), donc on l'inverse
    return (pv, dv[::-1])
