from .base import DAG


class Number(DAG):
    """
    Represent a constant numerical leaf in the computation graph.

    Attributes:
        value (float): The constant numerical value.
    """

    __slots__ = ("value",)
    _cache: dict[float, "Number"] = {}

    def __init__(self, value: float) -> None:
        """Initialize a new constant numerical leaf."""
        self.value = value

    @staticmethod
    def make(value: float | int) -> "Number":
        """
        Create a new Number node or retrieve it from cache (Flyweight pattern).

        Args:
            value (float | int): The numerical value to wrap.

        Returns:
            Number: A normalized and cached Number instance.
        """

        # 1. Normalize value to 12 decimal places to handle float precision
        # and ensure consistent cache keys.
        value = round(float(value), 12)

        try:
            # 2. Fast Path: Attempt to retrieve from cache immediately.
            # This is highly optimized for frequently used values like 0.0 or 1.0.
            return Number._cache[value]

        except KeyError:
            # 3. Slow Path: Create, store and return a new instance.
            node = Number(value)
            Number._cache[value] = node
            return node

    def substitute(self, env: dict[str, "DAG"]) -> "Number":
        """
        Perform a symbolic replacement on this constant.

        Since a literal number is invariant and does not depend on any variables,
        substitution has no effect and simply returns the node itself.

        Args:
            env (dict[str, Any]): The substitution environment (ignored).

        Returns:
            Number: The current node (self).
        """
        return self

    def evaluate(self, env: dict[str, float], memo: dict) -> float:
        """
        Reduce the constant to its literal numerical value.

        This represents the "terminal" step of an evaluation where the stored
        float is finally extracted for numerical computation.

        Args:
            env (dict[str, float]): The numerical environment (ignored).
            memo (dict): Evaluation cache (kept for interface consistency).

        Returns:
            float: The actual float value stored in this node.
        """
        return self.value

    def _compute_partial_derivative(self, name: str) -> "Number":
        """
        Compute the partial derivative of this constant with respect to 'name'.

        Applying the constant rule of differentiation:
        $\frac{\partial c}{\partial x} = 0$ for any constant $c$.

        Args:
            name (str): The variable name to differentiate against.

        Returns:
            Number: The global constant node ZERO.
        """
        # Derivative of a constant number is always zero.
        return ZERO

    def _compute_polynomial(self, env):
        """
        Convert the numerical constant into a constant (degree-0) polynomial.

        In the polynomial engine, a scalar $c$ is represented as $P(t) = c$.
        This is the base case for building complex polynomials from the DAG.

        Args:
            env (dict[str, Any]): The substitution environment (ignored).

        Returns:
            Polynomial: A polynomial where the only coefficient is the node's value.
        """
        from ..Polynomial import Polynomial

        # On crée un polynôme constant : [value] représente c * t^0
        self._poly_cache = (p := Polynomial([self.value]))
        return p

    def __str__(self) -> str:
        """
        Return the string representation of the constant value.

        Returns:
            str: The literal value formatted as a string.
        """
        return f"{self.value}"

    def __hash__(self) -> int:
        """
        Compute and cache the structural hash for this numerical node.

        Since Number nodes are terminal leaves in the DAG, the hash is
        derived strictly from their type and numerical value.

        Returns:
            int: The cached or newly computed hash.
        """
        try:
            return self._hash_cache
        except AttributeError:

            self._hash_cache = (h := hash((type(self), self.value)))
            return h


MINUS_ONE = Number.make(-1.0)
ZERO = Number.make(0.0)
ONE = Number.make(1.0)
