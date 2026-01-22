def hd(A):
    # print(A)
    # (h, t) = A
    # return h
    if not A:
        return None
    return A[0]


def tl(A):
    # (h, t) = A
    # return t
    return A[1:]


def tof(a):
    return a.t


def union(A, B):
    if None == A:
        return B

    elif None == B:
        return A

    else:
        (ta, qa) = (hd(A), tl(A))
        (tb, qb) = (hd(B), tl(B))
        (a1, a2) = (tof(ta.a), tof(ta.b))
        (b1, b2) = (tof(tb.a), tof(tb.b))

        assert a1 <= a2
        assert b1 <= b2

        if a1 > b1:
            return union(B, A)

        assert a1 <= b1

        # ils ne se touchent pas
        if a2 < b1:
            return (ta, (union(tl(A), B)))

        assert a2 >= b1

        if b2 <= a2:
            return union((ta, tl(A)), tl(B))

        else:
            return union(union((a1, b2), tl(A)), tl(B))


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


def inter(A, B):
    if None == A or None == B:
        return None
    if not A or not B:
        return None
    else:
        (ta, qa) = (hd(A), tl(A))
        (tb, qb) = (hd(B), tl(B))

        if ta is None or tb is None:
            return None

        (a1, a2) = (ta.a.t, ta.b.t)
        (b1, b2) = (tb.a.t, tb.b.t)

        assert a1 <= a2
        assert b1 <= b2

        if a1 > b1:
            return inter(B, A)

        elif a2 < b1:
            return inter(qa, B)

        elif b2 <= a2:
            return ((b1, b2), inter(A, qb))

        else:
            return ((b1, a2), inter(qa, B))


if __name__ == "__main__":
    A = [[0, 5]]
    B = [[3, 8]]

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

        assert a1 <= a2  #
        assert b1 <= b2  #

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

    print(f"\n Résultat: {union1D(A, B)}")
