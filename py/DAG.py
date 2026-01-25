from Polynome import *


class M(object):
    __slots__ = ()

    def __init__(self):
        " "

    def __neg__(self):
        """Surcharge de l'opérateur unaire '-' (ex: -Var('x'))"""

        if isinstance(self, Nb):
            return Nb(-self.nb)

        if isinstance(self, Opp):
            return self.a

        return Opp(self)

    def __add__(self, b):

        # Nb(0) + b -> b
        if isinstance(self, Nb) and self.nb == 0:
            return b

        # self + Nb(0) -> self
        if isinstance(b, Nb) and b.nb == 0:
            return self

        if isinstance(self, Nb) and isinstance(b, Nb):
            return Nb(self.nb + b.nb)

        return Plus(self, b)

    def __mul__(self, b):
        # Nb(1) * b -> b
        if isinstance(self, Nb) and self.nb == 1:
            return b

        # self * Nb(1) -> self
        if isinstance(b, Nb) and b.nb == 1:
            return self

        # Nb(0) * b -> Nb(0)
        if isinstance(self, Nb) and self.nb == 0:
            return Nb(0.0)

        # self * Nb(0) -> Nb(0)
        if isinstance(b, Nb) and b.nb == 0:
            return Nb(0.0)

        if isinstance(self, Nb) and isinstance(b, Nb):
            return Nb(self.nb * b.nb)

        return Mult(self, b)

    def __sub__(self, b):
        return self + (-b)


class Opp(M):
    __slots__ = "a"

    def __init__(self, a):
        self.a = a

    def eval(self, dico):
        return -self.a.eval(dico)

    def evalsymb(self, dico):
        return -self.a.evalsymb(dico)

    def topolent(self):
        return -self.a.topolent()

    def derivee(self, nom):
        return -self.a.derivee(nom)

    def to_poly(self, dico):
        p = self.a.to_poly(dico)
        return Polynome([-c for c in p.c])

    def __str__(self):
        return f"(-{self.a})"


class Plus(M):
    __slots__ = ("a", "b")

    def __init__(self, a, b):
        self.a = a
        self.b = b

    def eval(self, dico):
        return self.a.eval(dico) + self.b.eval(dico)

    def evalsymb(self, dico):
        return self.a.evalsymb(dico) + self.b.evalsymb(dico)

    def derivee(self, nom):
        return self.a.derivee(nom) + self.b.derivee(nom)

    def topolent(self):
        return self.a.topolent() + self.b.topolent()

    def __str__(self):
        return f"({self.a} + {self.b})"

    def to_poly(self, dico):
        return self.a.to_poly(dico) + self.b.to_poly(dico)


class Mult(M):
    __slots__ = ("a", "b")

    def __init__(self, a, b):
        self.a = a
        self.b = b

    def eval(self, dico):
        return self.a.eval(dico) * self.b.eval(dico)

    def evalsymb(self, dico):
        return self.a.evalsymb(dico) * self.b.evalsymb(dico)

    def derivee(self, nom):
        return self.a.derivee(nom) * self.b + self.a * self.b.derivee(nom)

    def topolent(self):
        return self.a.topolent() * self.b.topolent()

    def to_poly(self, dico):
        # On multiplie directement les polynômes
        return self.a.to_poly(dico) * self.b.to_poly(dico)

    def __str__(self):
        return f"({self.a} * {self.b})"


class Nb(M):
    __slots__ = "nb"

    def __init__(self, n):
        self.nb = n

    def eval(self, dico):
        return self.nb

    def evalsymb(self, dico):
        return self

    def derivee(self, nom):
        return Nb(0.0)

    def topolent(self):
        return Polynome([self.nb])

    def to_poly(self, dico):
        # Un nombre devient un polynôme constant [n]
        return Polynome([self.nb])

    def __str__(self):
        return f"{self.nb}"


class Var(M):
    __slots__ = "nom"

    def __init__(self, nom):
        self.nom = nom

    def eval(self, dico):
        if self.nom in dico:
            return dico.get(self.nom)

        else:
            return Var(self.nom)

    def derivee(self, nom):
        if self.nom == nom:
            return Nb(1.0)

        else:
            return Nb(0.0)

    def evalsymb(self, dico):
        if self.nom in dico:
            return dico.get(self.nom)

        else:
            return self

    def topolent(self):
        if self.nom == "t":
            return Polynome([0.0, 1.0])

    def to_poly(self, dico):
        return dico.get(self.nom)

    def __str__(self):
        return f"{self.nom}"
