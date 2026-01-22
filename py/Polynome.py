class Polynome:
    count__init__ = 0
    count__len = 0
    count__len__ = 0
    count__coeff = 0
    count__vect = 0
    count__img = 0
    count__add__ = 0
    count__mul__ = 0
    count__sub__ = 0
    count__opp__ = 0

    def __init__(self, c):
        Polynome.count__init__ += 1
        self.c = c
        self.len = len(self.c)

    def vect(self):
        Polynome.count__vect += 1
        return self.c

    def __call__(self, x):
        Polynome.count__img += 1

        n = self.len

        value = self.c[n - 1]

        for i in range(n - 2, -1, -1):
            value = value * x + self.c[i]

        return value

    def __add__(self, Q):
        Polynome.count__add__ += 1

        if self.len > Q.len:
            grand, petit = self, Q
        else:
            grand, petit = Q, self

        Z = list(grand.c)

        for i in range(petit.len):
            Z[i] += petit.c[i]

        return Polynome(Z)

    def __mul__(self, Q):
        Polynome.count__mul__ += 1

        len_self = self.len
        len_Q = Q.len

        mul_coeffs = [0] * (len_self + len_Q - 1)

        for i in range(len_self):
            c1 = self.c[i]

            if c1 == 0:
                continue

            for j in range(len_Q):
                mul_coeffs[i + j] += c1 * Q.c[j]

        return Polynome(mul_coeffs)

    def __sub__(self, Q):
        Polynome.count__sub__ += 1

        # Cas A : P est plus long ou égal à Q
        if self.len >= Q.len:
            Z = list(self.c)
            # On soustrait juste la partie commune
            for i in range(Q.len):
                Z[i] -= Q.c[i]

        # Cas B : Q est plus long que P
        else:
            Z = list(self.c)
            # 1. On soustrait la partie commune
            for i in range(self.len):
                Z[i] -= Q.c[i]
            # 2. On ajoute l'opposé de ce qui reste de Q (car 0 - Q[i])
            for i in range(self.len, Q.len):
                Z.append(-Q.c[i])

        return Polynome(Z)

    def __neg__(self):
        Polynome.count__opp__ += 1
        return Polynome([-c for c in self.c])

    def __str__(self):
        return f"Polynome({self.c})"
