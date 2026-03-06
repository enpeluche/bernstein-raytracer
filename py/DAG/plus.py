from .base import DAG
from .number import ZERO, ONE

from collections import defaultdict


class Plus(DAG):
    """
    Represent an N-ary addition operation in the computation graph.

    This node implements algebraic simplification (clustering identical monomials)
    and canonicalization to ensure equivalent expressions share the same structure.

    Attributes:
        args (tuple[DAG, ...]): The sequence of terms to be added.
    """

    __slots__ = ("args",)
    _cache = {}

    def __init__(self, args: tuple[DAG, ...]) -> None:
        """
        Initialize a summation node.

        Args:
            args (tuple[DAG, ...]): A tuple containing the terms to be added.
        """

        self.args = args

    @staticmethod
    def _split_coeff(term):
        from .number import Number
        from .mult import Mult

        """Sépare un terme en (coefficient_réel, reste_DAG)."""

        if isinstance(term, Number):
            return term.value, ONE

        if isinstance(term, Mult):
            coeff = 1.0
            rest = []
            for a in term.args:
                if isinstance(a, Number):
                    coeff *= a.value
                else:
                    rest.append(a)

            if not rest:
                return coeff, ONE
            if len(rest) == 1:
                return coeff, rest[0]
            # On utilise Mult.make pour le reste pour rester dans le cache

            return coeff, Mult.make(*rest)

        return 1.0, term

    @staticmethod
    def _flatten_args(args):
        from .number import Number

        flat = []
        constant_sum = 0.0

        for arg in args:

            if isinstance(arg, Plus):
                flat.extend(arg.args)
                continue

            if isinstance(arg, Number):
                constant_sum += arg.value
                continue

            if isinstance(arg, (int, float)):
                constant_sum += arg
                continue

            flat.append(arg)

        return flat, constant_sum

    @staticmethod
    def _aggregate_monomials(flat, constant_sum):
        from .number import Number
        from .mult import Mult

        # 2️⃣ Regroupement des monômes
        monomials = defaultdict(float)

        for term in flat:

            coeff, mono = Plus._split_coeff(term)

            if mono is ONE:
                constant_sum += coeff
                continue

            monomials[mono] += coeff

        return monomials, constant_sum

    @staticmethod
    def _reconstruct_terms(monomials, constant_sum):
        from .number import Number
        from .mult import Mult
        from .opp import Opp

        # 3️⃣ Reconstruction
        new_terms = []

        for mono, coeff in monomials.items():

            if coeff == 0:
                continue

            elif coeff == 1:
                new_terms.append(mono)

            elif coeff == -1:
                new_terms.append(Opp.make(mono))
            else:
                new_terms.append(Mult.make(Number.make(coeff), mono))

        # Ajouter constante finale
        if constant_sum != 0:
            new_terms.append(Number.make(constant_sum))

        return new_terms

    @staticmethod
    def _try_extract_common_factor(new_terms):

        from .number import Number
        from .mult import Mult
        from .pow import Pow
        from .plus import Plus

        if len(new_terms) <= 1:
            return None

        # --------
        # 1. Décomposition des termes en facteurs
        # --------
        term_factors = []

        for term in new_terms:

            coeff, mono = Plus._split_coeff(term)

            factors = {}

            if mono is ONE:
                factors = {}

            elif isinstance(mono, Mult):
                for a in mono.args:
                    if isinstance(a, Pow):
                        factors[a.base] = factors.get(a.base, 0) + a.exp
                    else:
                        factors[a] = factors.get(a, 0) + 1

            elif isinstance(mono, Pow):
                factors[mono.base] = mono.exp

            else:
                factors[mono] = 1

            term_factors.append((coeff, factors))

        import math

        coeffs = [abs(c) for c, _ in term_factors]

        common_coeff = coeffs[0]
        for c in coeffs[1:]:
            common_coeff = math.gcd(int(common_coeff), int(c))

        # --------
        # 2. Intersection des facteurs
        # --------
        common = term_factors[0][1].copy()

        for _, factors in term_factors[1:]:
            for base in list(common.keys()):
                if base in factors:
                    common[base] = min(common[base], factors[base])
                else:
                    del common[base]

        if not common and common_coeff == 1:
            return None

        # --------
        # 3. Reconstruction du facteur commun
        # --------
        common_factors = []

        if common_coeff != 1:
            common_factors.append(Number.make(common_coeff))

        for base, exp in common.items():
            if exp == 1:
                common_factors.append(base)
            else:
                common_factors.append(Pow.make(base, exp))

        common_factor = Mult.make(*common_factors)

        # --------
        # 4. Division des termes par le facteur commun
        # --------
        stripped_terms = []

        for coeff, factors in term_factors:

            coeff = coeff / common_coeff

            new_factors = []

            for base, exp in factors.items():

                new_exp = exp - common.get(base, 0)

                if new_exp == 1:
                    new_factors.append(base)
                elif new_exp > 1:
                    new_factors.append(Pow.make(base, new_exp))

            if new_factors:
                stripped = Mult.make(Number.make(coeff), *new_factors)
            else:
                stripped = Number.make(coeff)

            stripped_terms.append(stripped)

        inner_plus = Plus.make(*stripped_terms)

        return Mult.make(common_factor, inner_plus)

    @staticmethod
    def make(*args):

        flat, constant_sum = Plus._flatten_args(args)

        monomials, constant_sum = Plus._aggregate_monomials(flat, constant_sum)

        new_terms = Plus._reconstruct_terms(monomials, constant_sum)

        # 4️⃣ Cas dégénérés
        if not new_terms:
            return ZERO

        if len(new_terms) == 1:
            return new_terms[0]

        new_terms = tuple(
            sorted(new_terms, key=str)
        )  # 5️⃣ Canonicalisation (ordre stable)

        factored = Plus._try_extract_common_factor(new_terms)

        if factored is not None:
            return factored

        if new_terms in Plus._cache:
            return Plus._cache[new_terms]

        node = Plus(new_terms)
        Plus._cache[new_terms] = node

        return node

    def substitute(self, env: dict[str, "DAG"]) -> "DAG":
        """
        Perform a symbolic replacement across all terms of the sum.

        This method recursively substitutes each operand in the summation.
        By using the factory 'make', it allows for on-the-fly algebraic
        simplifications (e.g., constant folding).

        Args:
            env (dict[str, Any]): A mapping from variable names to replacement nodes.

        Returns:
            DAG: A new Plus node (or a simplified result) containing substituted terms.
        """
        new_args = [c.substitute(env) for c in self.args]
        return Plus.make(*new_args)

    def evaluate(self, env: dict[str, float], memo: dict) -> float:
        """
        Numerically compute the sum of all operands.

        Traverses the children nodes, evaluates them to floats, and returns
        their total sum.

        Args:
            env (dict[str, float]): Dictionary mapping variable names to floats.
            memo (dict): Evaluation cache to prevent redundant sub-tree traversals.

        Returns:
            float: The numerical sum of all child nodes.
        """
        if self in memo:
            return memo[self]

        return sum(a.evaluate(env, memo) for a in self.args)

    def _compute_partial_derivative(self, name: str) -> "DAG":
        """
        Compute the partial derivative of the sum using the Linearity Rule.

        According to the Sum Rule in calculus:
        $\frac{\partial}{\partial x} \sum f_i = \sum \frac{\partial f_i}{\partial x}$

        Args:
            name (str): The variable name to differentiate against.

        Returns:
            DAG: A new node representing the sum of the partial derivatives.
        """
        return Plus.make(*(child.partial_derivative(name) for child in self.args))

    def _compute_polynomial(self, env):

        result = None

        for child in self.args:
            poly = child.to_polynomial(env)
            result = poly if result is None else result + poly

        self._poly_cache = result

        return self._poly_cache

    def __str__(self) -> str:
        return " + ".join(str(c) for c in self.args)
