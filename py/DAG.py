from Polynomial import *


class DAG:
    """
    Classe de base pour le Graphe Orienté Acyclique (Directed Acyclic Graph).
    Représente un nœud dans un arbre de calcul symbolique.
    """

    __slots__ = ()

    def __neg__(self):
        """Surcharge de l'opérateur unaire '-' (ex: -Var('x'))"""

        if isinstance(self, Nb):
            return Nb(-self.nb)

        if isinstance(self, Opp):
            return self.a

        return Opp(self)

    def __add__(self, b):
        """Surcharge de l'opérateur '+' avec simplification algébrique."""

        # 0 + b -> b
        if isinstance(self, Nb) and self.nb == 0:
            return b

        # a + 0 -> a
        if isinstance(b, Nb) and b.nb == 0:
            return self

        # Constante + Constante -> Constante évaluée
        if isinstance(self, Nb) and isinstance(b, Nb):
            return Nb(self.nb + b.nb)

        return Plus(self, b)

    def __mul__(self, b):
        """Surcharge de l'opérateur '*' avec simplification algébrique."""

        # 1 * b -> b
        if isinstance(self, Nb) and self.nb == 1:
            return b

        # a * 1 -> a
        if isinstance(b, Nb) and b.nb == 1:
            return self

        # 0 * b -> 0
        if isinstance(self, Nb) and self.nb == 0:
            return Nb(0.0)

        # a * 0 -> 0
        if isinstance(b, Nb) and b.nb == 0:
            return Nb(0.0)

        # Constante * Constante -> Constante évaluée
        if isinstance(self, Nb) and isinstance(b, Nb):
            return Nb(self.nb * b.nb)

        return Mult(self, b)

    def __sub__(self, b):
        """Surcharge de l'opérateur '-'."""
        return self + (-b)


class Opp(DAG):
    """Nœud représentant l'opposé mathématique d'une expression (-a)."""

    __slots__ = "a"

    def __init__(self, a):
        self.a = a

    def eval(self, dico):
        return -self.a.eval(dico)

    def evalsymb(self, dico):
        return -self.a.evalsymb(dico)

    def topolent(self):
        return -self.a.topolent()

    def partial(self, var):
        return -self.a.partial(var)

    def to_poly(self, dico):
        p = self.a.to_poly(dico)
        return Polynomial([-c for c in p.coefficients])

    def __str__(self):
        return f"(-{self.a})"


class Plus(DAG):
    """Nœud représentant l'addition de deux expressions (a + b)."""

    __slots__ = ("a", "b")

    def __init__(self, a, b):
        self.a = a
        self.b = b

    def eval(self, dico):
        return self.a.eval(dico) + self.b.eval(dico)

    def evalsymb(self, dico):
        return self.a.evalsymb(dico) + self.b.evalsymb(dico)

    def partial(self, var):
        # La dérivée d'une somme est la somme des dérivées : (a + b)' = a' + b'
        return self.a.partial(var) + self.b.partial(var)

    def topolent(self):
        return self.a.topolent() + self.b.topolent()

    def __str__(self):
        return f"({self.a} + {self.b})"

    def to_poly(self, dico):
        return self.a.to_poly(dico) + self.b.to_poly(dico)


class Mult(DAG):
    """Nœud représentant la multiplication de deux expressions (a * b)."""

    __slots__ = ("a", "b")

    def __init__(self, a, b):
        self.a = a
        self.b = b

    def eval(self, dico):
        return self.a.eval(dico) * self.b.eval(dico)

    def evalsymb(self, dico):
        return self.a.evalsymb(dico) * self.b.evalsymb(dico)

    def partial(self, var):
        # Règle du produit : (a * b)' = a'b + ab'
        return self.a.partial(var) * self.b + self.a * self.b.partial(var)

    def topolent(self):
        return self.a.topolent() * self.b.topolent()

    def to_poly(self, dico):
        return self.a.to_poly(dico) * self.b.to_poly(dico)

    def __str__(self):
        return f"({self.a} * {self.b})"


class Nb(DAG):
    """Feuille du graphe représentant une constante numérique."""

    __slots__ = "nb"

    def __init__(self, n):
        self.nb = n

    def eval(self, dico):
        return self.nb

    def evalsymb(self, dico):
        return self

    def partial(self, var):
        # La dérivée d'une constante est 0
        return Nb(0.0)

    def topolent(self):
        return Polynomial([self.nb])

    def to_poly(self, dico):
        # Un nombre devient un polynôme constant [n]
        return Polynomial([self.nb])

    def __str__(self):
        return f"{self.nb}"


class Var(DAG):
    """Feuille du graphe représentant une variable symbolique (ex: 'x', 'y', 'z')."""

    __slots__ = "var"

    def __init__(self, var):
        self.var = var

    def eval(self, dico):
        if self.var in dico:
            return dico.get(self.var)

        else:
            return Var(self.var)

    def partial(self, var):
        # La dérivée de x par rapport à x est 1. Par rapport à y, c'est 0.
        if self.var == var:
            return Nb(1.0)

        else:
            return Nb(0.0)

    def evalsymb(self, dico):
        if self.var in dico:
            return dico.get(self.var)

        else:
            return self

    def topolent(self):
        if self.var == "t":
            return Polynomial([0.0, 1.0])

    def to_poly(self, dico):
        return dico.get(self.var)

    def __str__(self):
        return f"{self.var}"
