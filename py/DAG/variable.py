from .base import DAG


class Variable(DAG):
    """
    Represent a symbolic variable leaf in the computation graph (e.g., 'x', 'y', 'z').

    Attributes:
        name (str): The unique identifier for the variable.
    """

    __slots__ = ("name",)
    _cache: dict[str, "Variable"] = {}

    def __init__(self, name: str) -> None:
        """
        Initialize a new symbolic Variable.

        Args:
            name (str): The unique identifier for the variable (e.g., 'x', 'y').
        """

        self.name = name

    @staticmethod
    def make(name: str) -> "Variable":
        """
        Retrieve a Variable node from cache or create a new one (String Interning).

        This ensures that a variable with the same name (e.g., 'x') is represented
        by a single unique instance throughout the entire computation graph.

        Args:
            name (str): The unique string identifier for the variable.

        Returns:
            Variable: The unique cached instance for this name.
        """

        try:
            # 1. Fast Path: Direct cache lookup.
            # Constant time O(1) access for existing variables.
            return Variable._cache[name]

        except KeyError:
            # 2. Slow Path: Create and register the new variable.
            node = Variable(name)
            Variable._cache[name] = node

            return node

    def substitute(self, env: dict[str, "DAG"]) -> "DAG":
        """
        Perform a symbolic replacement of this variable.

        This is used for high-level "algebraic surgery," such as replacing
        the generic coordinate 'x' with the ray equation $o_x + t \cdot d_x$.

        Args:
            env (dict[str, Any]): A mapping from variable names to replacement nodes.

        Returns:
            DAG: The replacement node if found in the env; otherwise, self.
        """
        return env.get(self.name, self)

    def evaluate(self, env: dict[str, float], memo: dict) -> float:
        """
        Reduce the variable to its numerical value.

        During the final rendering phase, this method pulls the actual float
        coordinates (like the value of 'ox' or 'D2') from the ray's environment.

        Args:
            env (dict[str, float]): Dictionary mapping variable names to floats.
            memo (dict): Evaluation cache (kept for consistency with the DAG interface).

        Returns:
            float: The numerical value of the variable, defaulting to 0.0.
        """
        return env.get(self.name, 0.0)

    def _compute_partial_derivative(self, name: str) -> "DAG":
        """
        Compute the partial derivative of this variable with respect to 'name'.

        Applying the fundamental rules of calculus:
        - $\frac{\partial v}{\partial v} = 1$
        - $\frac{\partial v}{\partial u} = 0$ (where $u \neq v$)

        Args:
            name (str): The variable name to differentiate against.

        Returns:
            DAG: The constant node ONE if names match, otherwise ZERO.
        """
        from .number import ONE, ZERO

        if self.name == name:
            return ONE
        return ZERO

    def _compute_polynomial(self, env):
        """
        Convert the symbolic variable into its polynomial representation.

        This method retrieves the polynomial mapping for this variable from the
        provided environment (e.g., mapping 'x' to the polynomial $o_x + t \cdot d_x$).
        The result is cached to avoid redundant lookups during DAG traversal.

        Args:
            env (dict[str, Polynomial]): The environment mapping variable names to polynomials.

        Returns:
            Polynomial: The polynomial equivalent of this variable.
        """
        p = env[self.name]
        self._poly_cache = p
        return p

    def __str__(self) -> str:
        """
        Return the string representation of the variable.

        Returns:
            str: The variable's name (e.g., 'x', 'y', 'z').
        """
        return f"{self.name}"

    def __hash__(self):
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
            self._hash_cache = (h := hash((type(self), self.name)))
            return h
