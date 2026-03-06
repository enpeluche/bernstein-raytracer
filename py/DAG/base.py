class DAG:
    """
    Base class for the Directed Acyclic Graph (DAG) nodes.

    This class provides the core infrastructure for symbolic computation,
    including memory optimization via slots and centralized caching mechanisms
    for hashes, derivatives, and polynomial conversions.

    All subclasses must implement their own simplification logic within
    a 'make' factory method to ensure graph minimality.
    """

    __slots__ = (
        "_poly_cache",
        "_hash_cache",
        "_derivative_cache",
    )

    @property
    def args(self):
        return ()

    def __eq__(self, other) -> bool:
        """
        Check structural equality using instance identity.

        Since nodes are cached and unique (Flyweight pattern),
        identity comparison is sufficient for equality.
        """

        return self is other

    def __neg__(self) -> "DAG":
        """
        Create a negation of the current expression.

        Returns:
            DAG: A simplified Opp node.
        """
        from .mult import Mult
        from .number import MINUS_ONE

        return Mult.make(MINUS_ONE, self)
        # from .opp import Opp
        # return Opp.make(self)

    def __add__(self, b) -> "DAG":
        """
        Create an addition node (self + other).

        Returns:
            DAG: A simplified Plus node.
        """

        from .plus import Plus

        return Plus.make(self, b)

    def __radd__(self, b) -> "DAG":
        """
        Handle reflected addition (other + self).
        """

        from .plus import Plus

        return Plus.make(b, self)

    def __sub__(self, b) -> "DAG":
        """
        Create a subtraction node by adding a negation.
        """

        return self + (-b)

    def __mul__(self, b) -> "DAG":
        """
        Create a multiplication node (self * other).

        Returns:
            DAG: A simplified Mult node.
        """

        from .mult import Mult

        return Mult.make(self, b)

    def __rmul__(self, b) -> "DAG":
        """
        Handle reflected multiplication (other * self).
        """

        from .mult import Mult

        return Mult.make(b, self)

    def __pow__(self, exponent: int) -> "DAG":
        """
        Create a power node (self ^ exponent).

        Returns:
            DAG: A simplified Pow node.
        """

        from .pow import Pow

        return Pow.make(self, exponent)

    def evaluate(self, env: dict, memo: dict) -> float:
        """
        Evaluate the node numerically. Must be implemented by subclasses.
        """
        raise NotImplementedError(
            f"La méthode evaluate manque dans {type(self).__name__}"
        )

    def partial_derivative(self, var: str) -> "DAG":
        """
        Compute and cache the partial derivative with respect to 'var'.
        Delegates the actual math to '_compute_partial_derivative' in subclasses.
        """
        try:
            cache = self._derivative_cache
        except AttributeError:
            cache = self._derivative_cache = {}

        if var in cache:
            return cache[var]

        res = self._compute_partial_derivative(var)

        cache[var] = res
        return res

    def to_polynomial(self, env):
        """
        Convert the DAG node into a Polynomial.
        Handles caching automatically to avoid redundant tree traversals.
        Delegates the actual conversion to '_compute_polynomial' in subclasses.
        """
        try:
            return self._poly_cache
        except AttributeError:
            res = self._compute_polynomial(env)
            self._poly_cache = res
            return res

    def __hash__(self) -> int:
        """
        Compute and cache the structural hash of the node.

        The hash is based on the node type and its arguments to ensure
        that structurally identical nodes produce the same hash value.

        Returns:
            int: The cached or newly computed hash code.
        """

        try:
            return self._hash_cache
        except AttributeError:
            self._hash_cache = hash((type(self), self.args))
            return self._hash_cache
