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
    if None == A:
        return None

    elif None == B:
        return A

    else:
        (ta, qa) = (hd(A), tl(A))
        (tb, qb) = (hd(B), tl(B))
        (a1, a2) = (ta.a.t, ta.b.t)
        (b1, b2) = (tb.a.t, tb.b.t)

        assert a1 <= a2
        assert b1 <= b2

        if b2 <= a1:
            return differ(A, tl(B))

        elif a2 <= b1:
            return ta, differ(tl(A), B)

        elif b1 <= a1:
            if b2 <= a2:
                return differ(((b2, a2), tl(A)), tl(B))

            else:
                return differ(tl(A), B)

        elif a2 <= b2:
            return ((a1, b1), differ(tl(A), B))

        else:
            return ((a1, b1), differ(((b2, a2), tl(A)), tl(B)))


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
    A = [[0, 2], [5, 10]]
    B = [[1, 9]]

    print(f"\n Résultat: {inter1D(A, B)}")
