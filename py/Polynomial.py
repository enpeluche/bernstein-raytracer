from Casteljau import *

from solveracine import solve
from math import sqrt

# fmt: off

CACHE_COEFF_BIN = [
    [1.0],
    [1.0,  1.0],
    [1.0,  2.0,  1.0],
    [1.0,  3.0,  3.0,   1.0],
    [1.0,  4.0,  6.0,   4.0,   1.0],
    [1.0,  5.0, 10.0,  10.0,   5.0,   1.0],
    [1.0,  6.0, 15.0,  20.0,  15.0,   6.0,   1.0],
    [1.0,  7.0, 21.0,  35.0,  35.0,  21.0,   7.0,   1.0],
    [1.0,  8.0, 28.0,  56.0,  70.0,  56.0,  28.0,   8.0,  1.0],
    [1.0,  9.0, 36.0,  84.0, 126.0, 126.0,  84.0,  36.0,  9.0, 1.0],
    [1.0, 10.0, 45.0, 120.0, 210.0, 252.0, 210.0, 120.0, 45.0, 10.0, 1.0],
]

# fmt: on


class Polynomial:
    __slots__ = ("coefficients", "len")

    def __init__(self, coefficients):
        """
        Create a Polynomial object (where c[0] is the constant term).

        Args:
            c (tuple[float]): coefficients of polynomial in ascending order of power.
        """

        coefficients = [float(x) for x in coefficients]

        while len(coefficients) > 1 and coefficients[-1] == 0:
            coefficients.pop()

        self.coefficients = tuple(coefficients)

        self.len = len(self.coefficients)

    def get_coefficients(self):
        return self.coefficients

    def __call__(self, x):
        """
        Implements Hörner methods.

        Args:
            x (float): a real number
        """

        n = self.len

        value = self.coefficients[n - 1]

        for i in range(n - 2, -1, -1):
            value = value * x + self.coefficients[i]

        return value

    def __add__(self, Q):

        if self.len > Q.len:
            grand, petit = self, Q
        else:
            grand, petit = Q, self

        Z = list(grand.coefficients)

        for i in range(petit.len):
            Z[i] += petit.coefficients[i]

        return Polynomial(Z)

    def __mul__(self, Q):

        len_self = self.len
        len_Q = Q.len

        mul_coeffs = [0] * (len_self + len_Q - 1)

        for i in range(len_self):
            c1 = self.coefficients[i]

            if c1 == 0:
                continue

            for j in range(len_Q):
                mul_coeffs[i + j] += c1 * Q.coefficients[j]

        return Polynomial(mul_coeffs)

    def __sub__(self, Q):

        if self.len >= Q.len:
            Z = list(self.coefficients)

            for i in range(Q.len):
                Z[i] -= Q.coefficients[i]

        else:
            Z = list(self.coefficients)

            for i in range(self.len):
                Z[i] -= Q.coefficients[i]

            for i in range(self.len, Q.len):
                Z.append(-Q.coefficients[i])

        return Polynomial(Z)

    def __neg__(self):

        return Polynomial([-c for c in self.coefficients])

    def reverse(self):
        return Polynomial(self.coefficients[::-1])

    def _clean(self):
        return Polynomial([round(c, 7) for c in self.coefficients])

    def roots(self):
        P = self
        epsilon = 1e-5

        if not P.coefficients:
            return []

        if len(P.coefficients) > 1 and P.coefficients[0] == 0:
            return Polynomial(P.coefficients[1:]).roots()

        if P.len == 1:
            return []  # pour le moment, pas satisfaiant

        if P.len == 2:
            return [-P.coefficients[0] / P.coefficients[1]]

        if P.len == 3:
            c = P.coefficients[0]
            b = P.coefficients[1]
            a = P.coefficients[2]

            if abs(a) < 1e-9:
                if abs(b) < 1e-9:
                    return []
                return [-c / b]

            delta = b * b - 4 * a * c

            if abs(delta) < 1e-10:
                t = -b / (2 * a)
                return [t]

            if delta < 0:
                return []

            sqrt_delta = sqrt(delta)

            t1 = (-b - sqrt_delta) / (2 * a)
            t2 = (-b + sqrt_delta) / (2 * a)

            return sorted([t1, t2])

        # on commence à sortir l'artillerie lourde

        solutions = []

        roots_near = solve(epsilon, P.to_bernstein_basis(), 0, 1.0, [])
        solutions.extend(roots_near)

        roots_far_inv = solve(epsilon, P.reverse().to_bernstein_basis(), 0, 1.0, [])

        roots_far = []
        for u in roots_far_inv:
            if abs(u) > epsilon:
                t = 1.0 / u

                if t > 1.0 + epsilon:
                    roots_far.append(t)

        solutions.extend(sorted(roots_far))

        if not solutions:
            return []
        solutions = list(sorted(set(round(s, 4) for s in solutions)))

        return solutions

    def to_bernstein_basis(self):
        pol = [0] * self.len

        for k in range(self.len):
            for i in range(k + 1):
                pol[k] += self.coefficients[i] * (
                    CACHE_COEFF_BIN[k][i] / CACHE_COEFF_BIN[self.len - 1][i]
                )

        return pol

    def __str__(self):

        return f"Polynomial({self.coefficients})"


if __name__ == "__main__":
    P = Polynomial((-1, 1))
    Q = Polynomial((-0.5, 1))
    R = Polynomial((-5, 1))
    print((P * Q * R).roots())
