class Polynome:
    def __init__(self, c):
        """
        Create a Polynomial with coefficients in ascending order of power.
        (where c[0] is the constant term).

        :param c: A list of real numbers.
        """

        self.c = c

        while len(self.c) > 1 and self.c[-1] == 0:
            self.c.pop()

        self.len = len(self.c)

    def vect(self):

        return self.c

    def __call__(self, x):
        """
        Implements Hörner methods.

        :param x: a real number
        """

        n = self.len

        value = self.c[n - 1]

        for i in range(n - 2, -1, -1):
            value = value * x + self.c[i]

        return value

    def __add__(self, Q):

        if self.len > Q.len:
            grand, petit = self, Q
        else:
            grand, petit = Q, self

        Z = list(grand.c)

        for i in range(petit.len):
            Z[i] += petit.c[i]

        return Polynome(Z)

    def __mul__(self, Q):

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

        if self.len >= Q.len:
            Z = list(self.c)

            for i in range(Q.len):
                Z[i] -= Q.c[i]

        else:
            Z = list(self.c)

            for i in range(self.len):
                Z[i] -= Q.c[i]

            for i in range(self.len, Q.len):
                Z.append(-Q.c[i])

        return Polynome(Z)

    def __neg__(self):

        return Polynome([-c for c in self.c])

    def __str__(self):

        return f"Polynome({self.c})"
