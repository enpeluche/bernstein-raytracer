from .base import DAG
from .number import ONE


class Pow(DAG):
    """
    Represent a power operation (base raised to an exponent) in the computation graph.

    Attributes:
        base (DAG): The base expression node.
        exp (float): The constant numerical exponent.
    """

    __slots__ = (
        "base",
        "exp",
    )
    _cache = {}

    def __init__(self, base: DAG, exp: int) -> None:
        """
        Initialize a power node (base^exp).

        Args:
            base (DAG): The base expression node.
            exp (int): The constant exponent value.
        """

        self.base = base
        self.exp = int(exp)

    @property
    def args(self):
        return (self.base,)

    @staticmethod
    def make(base: DAG, exp: int) -> DAG:
        """
        Create a power node with algebraic simplifications and structural caching.

        This method applies several reduction rules:
        1. Exponent of 0 -> Number(1.0)
        2. Exponent of 1 -> Returns the base
        3. Constant folding -> If base and exp are numbers, returns a Number
        4. Power of power -> (x^a)^b = x^(a*b)

        Args:
            base (DAG): The base expression.
            exp (int): The numerical exponent.

        Returns:
            DAG: A simplified node (Number, original base, or a Pow instance).
        """

        from .number import Number

        def get_val(x):
            """Helper to extract a float value from a number or a literal."""
            if isinstance(x, Number):
                return x.value
            if isinstance(x, (int, float)):
                return float(x)
            return None

        base_val = get_val(base)
        exp_val = int(exp)

        if exp_val is not None:
            # Rule: x^0 = 1
            if exp_val == 0.0:
                return ONE

            # Rule: x^1 = x
            if exp_val == 1.0:
                return base if not isinstance(base, float) else Number.make(base)

            # Rule: Constant Folding (2^3 = 8)
            if base_val is not None:
                return Number.make(base_val ** exp_val)

            # Rule: Power of a Power (x^a)^b = x^(a*b)
            if isinstance(base, Pow):
                return Pow.make(base.base, base.exp * exp_val)

        # Structural Caching (Flyweight Pattern)
        key = (base, exp_val)
        try:
            return Pow._cache[key]
        except KeyError:
            new_node = Pow(base, exp_val)
            Pow._cache[key] = new_node
            return new_node

    def substitute(self, env: dict[str, "DAG"]) -> "DAG":
        """
        Perform a symbolic replacement in the base of the power.

        In this engine, exponents are treated as fixed numerical values.
        The substitution is recursively applied to the base node, then
        re-wrapped in a power operation via the 'make' factory.

        Args:
            env (dict[str, Any]): A mapping from variable names to replacement nodes.

        Returns:
            DAG: A new node representing the substituted power expression.
        """
        return Pow.make(self.base.substitute(env), self.exp)

    def evaluate(self, env: dict[str, float], memo: dict) -> float:
        """
        Numerically compute the power of the evaluated base.

        Args:
            env (dict[str, float]): Dictionary mapping variable names to floats.
            memo (dict): Evaluation cache to prevent redundant sub-tree traversals.

        Returns:
            float: The numerical result of $base^{exp}$.
        """
        return self.base.evaluate(env, memo) ** self.exp

    def _compute_partial_derivative(self, name: str) -> "DAG":
        """
        Compute the partial derivative using the Power Rule.

        Applying the generalized power rule:
        $\frac{\partial}{\partial x}(f^n) = n \cdot f^{n-1} \cdot \frac{\partial f}{\partial x}$

        Args:
            name (str): The variable name to differentiate against.

        Returns:
            DAG: A symbolic expression representing the derivative.
        """
        from .number import Number

        # n * f' * f**(n-1)
        return (
            Number.make(self.exp)
            * self.base.partial_derivative(name)
            * (self.base ** (self.exp - 1))
        )

    def _compute_polynomial(self, env):
        """
        Compute the polynomial expansion of the base expression raised to the exponent.

        Convert the base node into its polynomial form and perform iterative
        multiplication to satisfy the power operation. Optimized to handle identity
        cases for exponents 0 and 1.

        Algebraically:
        Given $P(t) = \text{base.to\_polynomial}(env)$, calculate $R(t) = P(t)^n$
        where $n$ is the fixed integer exponent.

        Args:
            env (dict[str, Polynomial]): The environment mapping variable names
                to their respective polynomial representations.

        Returns:
            Polynomial: The expanded polynomial result.
        """

        from Polynomial import POLY_ONE

        # 1. On récupère le polynôme de la base (ex: x + 1 -> [1, 1])
        base_poly = self.base.to_polynomial(env)

        # 2. Cas particuliers pour la performance
        if self.exp == 0:
            result = POLY_ONE

        elif self.exp == 1:
            result = base_poly

        else:
            # 3. Élévation à la puissance
            # On part de l'unité (polynôme [1.0])
            result = POLY_ONE

            # On multiplie 'exp' fois.
            for _ in range(self.exp):
                result = result * base_poly

        self._poly_cache = result

        return result

    def __str__(self) -> str:
        from .plus import Plus
        from .mult import Mult

        # On protège la base si c'est un Plus ou un Mult
        if isinstance(self.base, (Plus, Mult)):
            base_str = f"({self.base})"
        else:
            base_str = str(self.base)

        return f"{base_str}**{self.exp}"
