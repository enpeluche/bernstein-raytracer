from .base import DAG
from .number import ZERO, ONE

from collections import defaultdict


class Mult(DAG):
    """
    Represent an N-ary multiplication operation in the computation graph.

    This node implements algebraic reduction, such as constant folding,
    multiplication by zero, and merging of numerical coefficients.

    Attributes:
        args (tuple[DAG, ...]): The sequence of factors to be multiplied.
    """

    __slots__ = ("args",)
    _cache = {}

    def __init__(self, args: tuple[DAG, ...]) -> None:
        """
        Initialize a multiplication node.

        Args:
            args (tuple[DAG, ...]): A tuple containing the factors to be multiplied.
        """

        self.args = args

    @staticmethod
    def _flatten_args(args):
        from .number import Number

        flat = []
        constant_prod = 1

        for arg in args:

            # Mult imbriqués → flatten
            if isinstance(arg, Mult):
                flat.extend(arg.args)
                continue

            # Number
            if isinstance(arg, Number):
                if arg.value == 0:
                    return ZERO, 0.0
                constant_prod *= arg.value
                continue

            # int / float natif
            if isinstance(arg, (int, float)):
                if arg == 0:
                    return ZERO, 0.0
                constant_prod *= arg
                continue

            flat.append(arg)

        # produit nul
        if constant_prod == 0:
            return ZERO, 0.0

        return flat, constant_prod

    @staticmethod
    def _aggregate_powers(flat):
        # -------------------------
        # 2) Regroupement des bases
        #    x * x^2 → x^3
        # -------------------------
        from .pow import Pow

        power_count = defaultdict(int)

        for factor in flat:
            if isinstance(factor, Pow):
                power_count[factor.base] += factor.exp
            else:
                power_count[factor] += 1

        return power_count

    @staticmethod
    def _reconstruct_factors(power_count):
        from .pow import Pow
        from .number import Number

        # -------------------------
        # 3) Reconstruction facteurs
        # -------------------------
        new_factors = []

        for base, exp in power_count.items():

            # base^0 = 1
            if exp == 0:
                continue

            # base^1 = base
            if exp == 1:
                new_factors.append(base)

            else:
                new_factors.append(Pow.make(base, exp))

        return new_factors

    @staticmethod
    def _apply_identity_rules(new_factors, constant_prod):
        from .number import Number

        # -------------------------
        # 4) Ajouter constante
        # -------------------------
        if constant_prod != 1:
            new_factors.append(Number.make(constant_prod))

        # rien ?
        if not new_factors:
            return ONE

        # un seul facteur
        if len(new_factors) == 1:
            return new_factors[0]

        return new_factors

    @staticmethod
    def make(*args):

        flat, constant_prod = Mult._flatten_args(args)

        if flat is ZERO:
            return ZERO

        power_count = Mult._aggregate_powers(flat)

        new_factors = Mult._reconstruct_factors(power_count)

        result = Mult._apply_identity_rules(new_factors, constant_prod)

        if not isinstance(result, list):
            return result

        new_factors = result

        new_factors = tuple(sorted(new_factors, key=str))  # 5) Ordre canonique DAG

        if new_factors in Mult._cache:
            return Mult._cache[new_factors]

        node = Mult(new_factors)
        Mult._cache[new_factors] = node

        return node

    def substitute(self, env):
        new_args = [c.substitute(env) for c in self.args]
        # .make() va s'occuper de simplifier (0 * x, 1 * x, etc.)
        return Mult.make(*new_args)

    def evaluate(self, env, memo):
        if self in memo:
            return memo[self]

        res = 1
        for a in self.args:
            res *= a.evaluate(env, memo)
        return res

    def _compute_partial_derivative(self, var):
        from .number import Number
        from .plus import Plus

        terms = []

        for i, child in enumerate(self.args):

            derived = child.partial_derivative(var)

            if isinstance(derived, Number) and derived.value == 0:
                continue

            factors = list(self.args)
            factors[i] = derived

            terms.append(Mult.make(*factors))

        return Plus.make(*terms)

    def _compute_polynomial(self, env):
        """
        Convertit le produit N-aire en un seul polynôme.
        Multiplie récursivement les polynômes de tous les enfants.
        """

        # On commence avec le polynôme du premier enfant
        res = self.args[0].to_polynomial(env)

        # On multiplie successivement par les autres
        for i in range(1, len(self.args)):
            res = res * self.args[i].to_polynomial(env)

        self._poly_cache = res

        return self._poly_cache

    def __str__(self) -> str:
        from .plus import Plus

        parts = []
        for arg in self.args:
            # Si le facteur est une addition, on le protège avec des parenthèses
            if isinstance(arg, Plus):
                parts.append(f"({arg})")
            else:
                parts.append(str(arg))

        return " * ".join(parts)
