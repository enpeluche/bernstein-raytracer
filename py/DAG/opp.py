from .base import DAG


class Opp(DAG):
    """
    Represent a unary negation operation (-x) in the computation graph.

    Attributes:
        _args (DAG): The single expression node being negated.
    """

    __slots__ = ("arg",)
    _cache = {}

    def __init__(self, arg: DAG) -> None:
        """
        Initialize a negation node (-x).

        Args:
            arg (DAG): The expression node to negate.
        """

        self.arg = arg

    @property
    def args(self):
        return (self.arg,)

    @staticmethod
    def make(node: DAG) -> DAG:
        """
        Create a negation node with algebraic simplification and caching.

        Simplification rules:
        1. Constant Folding: -Number(x) -> Number(-x)
        2. Double Negation: -(-x) -> x

        Args:
            node (DAG): The expression node to negate.

        Returns:
            DAG: A simplified node (Number, original inner node, or Opp instance).
        """

        from .number import Number

        # Rule 1: Constant Folding
        if isinstance(node, Number):
            return Number.make(-node.value)

        # Rule 2: Double Negation Elimination -(-x) = x
        # Note: We access the inner node via 'arg' (or your specific attribute name)
        if isinstance(node, Opp):
            return node.arg

        # Structural Caching (Flyweight Pattern)
        try:
            return Opp._cache[node]
        except KeyError:
            new_node = Opp(node)
            Opp._cache[node] = new_node
            return new_node

    def substitute(self, env: dict[str, "DAG"]) -> "DAG":
        """
        Perform a symbolic replacement on the negated expression.

        This method propagates the substitution to the underlying child node
        and re-wraps the result in a negation to maintain the algebraic structure.

        Args:
            env (dict[str, Any]): A mapping from variable names to replacement nodes.

        Returns:
            DAG: A new negated node containing the substituted expression.
        """
        return Opp.make(self.arg.substitute(env))

    def evaluate(self, env: dict[str, float], memo: dict) -> float:
        """
        Numerically evaluate the negation of the child node.

        First, it computes the float value of the underlying expression,
        then applies the unary minus operator.

        Args:
            env (dict[str, float]): Dictionary mapping variable names to floats.
            memo (dict): Evaluation cache to avoid redundant calculations.

        Returns:
            float: The negated numerical result ($-f(x)$).
        """
        return -self.arg.evaluate(env, memo)

    def _compute_partial_derivative(self, name: str) -> "DAG":
        """
        Compute the partial derivative of the negated expression.

        This follows the linearity rule of differentiation:
        $\frac{\partial}{\partial x}(-f) = - \left( \frac{\partial f}{\partial x} \right)$

        Args:
            name (str): The variable name to differentiate against.

        Returns:
            DAG: The negation of the child node's partial derivative.
        """
        return -self.arg.partial_derivative(name)

    def _compute_polynomial(self, env):
        """
        Compute the polynomial representation of the negated expression.

        This method propagates the polynomial conversion to the child node and
        negates the resulting coefficients to produce the additive inverse.

        Algebraically:
        If $P(t) = \sum_{i=0}^{n} c_i t^i$, then the result is $-P(t) = \sum_{i=0}^{n} (-c_i) t^i$.

        Args:
            env (dict[str, Polynomial]): The environment mapping variable names
                to their respective polynomial representations.

        Returns:
            Polynomial: A new polynomial with all coefficients negated.
        """

        from Polynomial import Polynomial

        P = self.arg.to_polynomial(env)

        self._poly_cache = Polynomial([-c for c in P.coefficients])

        return self._poly_cache

    def __str__(self) -> str:
        """
        Return the string representation of the negation.

        Returns:
            str: The child expression prefixed with a minus sign (e.g., '-x').
        """
        return f"-{self.arg}"
