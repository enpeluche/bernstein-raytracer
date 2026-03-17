from .number import Number
from .variable import Variable
from .plus import Plus
from .mult import Mult
from .pow import Pow
from .base import DAG
from .opp import Opp


def _dfs(node: DAG, visited: set[DAG], order: list[DAG]) -> None:
    """
    Traverse the DAG using a depth-first search to determine evaluation order.

    Visit each node recursively and mark it as visited to avoid redundant processing
    and handle shared sub-expressions. Append the node to the execution list only
    after all of its dependencies (children) have been processed (post-order traversal).

    Args:
        node: The current DAG node being visited.
        visited: A set tracking previously visited nodes to ensure each node is
            processed exactly once.
        order: A list that stores the nodes in their resolved topological order.
    """

    if node in visited:
        return

    visited.add(node)

    for a in node.args:
        _dfs(a, visited, order)

    order.append(node)


def topological_sort_forest(roots: list[DAG]) -> list[DAG]:
    """
    Perform a topological sort on a forest of multiple DAG roots.

    Flatten a collection of expression graphs into a single linear sequence.
    This method shares the visited state across all roots, ensuring that common
    sub-expressions (shared nodes) are only included once in the final order.

    Args:
        roots: A list of terminal nodes (roots) representing the forest to sort.

    Returns:
        A list of DAG nodes ordered from leaves to roots, suitable for
        linear evaluation or code generation.
    """

    visited = set()
    order = []

    for r in roots:
        _dfs(r, visited, order)

    return order


def topological_sort(root: DAG) -> list[DAG]:
    """Perform a topological sort on a single DAG.

    Convenience wrapper that converts a single root node into a forest
    to resolve its dependencies in post-order.

    Args:
        root: The terminal node of the mathematical expression graph.

    Returns:
        A list of nodes in topological order (leaves first, root last).
    """

    return topological_sort_forest([root])


def compile_dag_evaluator(
    roots: list[DAG], forced_args: list[str] | None
) -> tuple[callable, str]:

    """
    Compile a forest of DAG nodes into an optimized Python function.

    Perform a topological sort to linearize the expression graph and generate
    a flat Python function using 'exec'. This process eliminates recursive
    function call overhead and leverages Common Subexpression Elimination (CSE)
    by mapping each unique node to a single temporary variable.

    Args:
        roots: A list of DAG nodes representing the polynomial coefficients
            (the outputs of the function).
        forced_args: An optional list of string names to define the function's
            argument signature. If None, names are automatically extracted
            from the Variables found in the DAG.

    Returns:
        A tuple containing:
            - The compiled Python function (Callable).
            - The generated source code string for debugging or inspection.

    Raises:
        TypeError: If a node type in the DAG is not supported by the compiler.
    """

    # 1. Handle argument signature
    if forced_args:
        args_str = ", ".join(forced_args)
    else:
        all_nodes = set()
        for r in roots:
            all_nodes.update(topological_sort(r))
        vars_needed = sorted({n.name for n in all_nodes if isinstance(n, Variable)})
        args_str = ", ".join(vars_needed)

    # 2. Start function definition
    lines = [f"def evaluate_dags({args_str}):"]
    indent = "    "

    # 3. Linearize the forest and map nodes to temporary variables
    nodes = topological_sort_forest(roots)
    index = {node: i for i, node in enumerate(nodes)}

    for node in nodes:
        i = index[node]

        if isinstance(node, Number):
            lines.append(f"{indent}t{i} = {node.value}")

        elif isinstance(node, Variable):
            lines.append(f"{indent}t{i} = {node.name}")

        elif isinstance(node, Plus):
            args = [f"t{index[a]}" for a in node.args]
            lines.append(f"{indent}t{i} = {' + '.join(args)}")

        elif isinstance(node, Mult):
            args = [f"t{index[a]}" for a in node.args]
            lines.append(f"{indent}t{i} = {' * '.join(args)}")

        elif isinstance(node, Pow):
            base = f"t{index[node.base]}"
            lines.append(f"{indent}t{i} = {base} ** {node.exp}")

        elif isinstance(node, Opp):
            # L'opposition est unaire, on prend le premier (et seul) argument
            arg = f"t{index[node.args[0]]}"
            lines.append(f"{indent}t{i} = -{arg}")

        else:
            raise TypeError(f"Unknown node type {type(node)}")

    # 4. Return the calculated coefficients (roots)
    outputs = ", ".join(f"t{index[r]}" for r in roots)
    lines.append(f"{indent}return [{outputs}]")

    code = "\n".join(lines)
    namespace = {}
    exec(code, namespace)

    return namespace["evaluate_dags"], code


def optimize_patterns(dag_node):
    from .variable import Variable
    from .plus import Plus
    from .mult import Mult
    from .pow import Pow

    n2 = Number.make(2.0)
    # 1. Variables
    ox, oy, oz = Variable.make("ox"), Variable.make("oy"), Variable.make("oz")
    dx, dy, dz = Variable.make("dx"), Variable.make("dy"), Variable.make("dz")

    # Variables de remplacement
    O2_var = Variable.make("O2")
    D2_var = Variable.make("D2")
    OD_var = Variable.make("OD")

    # 2. Les patterns à chercher (en SETS pour chercher des sous-parties de l'addition !)
    o2_set = {Pow.make(ox, 2), Pow.make(oy, 2), Pow.make(oz, 2)}
    d2_set = {Pow.make(dx, 2), Pow.make(dy, 2), Pow.make(dz, 2)}
    od2_set = {Mult.make(n2, dx, ox), Mult.make(n2, dy, oy), Mult.make(n2, dz, oz)}

    # Le pattern OD (sans le 2.0 car ton moteur l'a brillamment factorisé)
    od_set = {Mult.make(dx, ox), Mult.make(dy, oy), Mult.make(dz, oz)}

    memo = {}

    def apply_replace(node):
        if node in memo:
            return memo[node]

        # --- A. On traite les enfants d'abord (Bottom-Up) ---
        if isinstance(node, (Plus, Mult, Pow)):
            if isinstance(node, Pow):
                node = type(node).make(apply_replace(node.base), node.exp)
            else:
                new_args = tuple(apply_replace(a) for a in node.args)
                node = type(node).make(*new_args)

        # --- B. Recherche des patterns dans les additions ---
        if isinstance(node, Plus):
            # On transforme les arguments en liste pour pouvoir les manipuler
            current_terms = list(node.args)

            def extract(target_set, replacement):
                # Si les termes qu'on cherche sont TOUS présents dans l'addition
                if target_set.issubset(set(current_terms)):
                    # On les supprime
                    for t in target_set:
                        current_terms.remove(t)
                    # On met la variable (ex: O2) à la place
                    current_terms.append(replacement)
                    return True
                return False

            matched = False
            matched |= extract(o2_set, O2_var)
            matched |= extract(d2_set, D2_var)
            matched |= extract(od_set, OD_var)
            matched |= extract(od2_set, Mult.make(n2, OD_var))

            # Si on a remplacé quelque chose, on recrée le nœud Plus
            if matched:
                if len(current_terms) == 1:
                    res = current_terms[0]
                else:
                    res = Plus.make(*current_terms)
            else:
                res = node
        else:
            res = node

        memo[node] = res
        return res

    return apply_replace(dag_node)


def analyze_primitive_compiler(implicit_function, surface_name, env):
    """
    Exécute une suite complète d'analyses et de logs pour une surface implicite
    pendant la phase de compilation JIT.
    """
    print("=" * 80)
    print(f"COMPILER SUITE: ANALYZING {surface_name}")
    print("=" * 80)

    print(f"\n[ PHASE 1 ] SYMBOLIC GEOMETRY")
    print(f"  • Implicit Equation : f(x, y, z) = {implicit_function}")

    dfx = implicit_function.partial_derivative("x")
    dfy = implicit_function.partial_derivative("y")
    dfz = implicit_function.partial_derivative("z")

    print(f"  • Gradient ∇f (Normal vectors) :")
    print(f"    ∂f/∂x : {dfx}")
    print(f"    ∂f/∂y : {dfy}")
    print(f"    ∂f/∂z : {dfz}")

    print(f"\n[ PHASE 2 ] RAY PARAMETERIZATION")
    print(f"  Substituting: P(t) = O + tD")
    print(f"  (x, y, z) ➔ (ox + t*dx, oy + t*dy, oz + t*dz)")

    poly = implicit_function.to_polynomial(env)  #
    print(f"\n  Resulting Polynomial P(t) coefficients (Raw):")
    for i, coeff in enumerate(poly.coefficients):
        print(f"    t^{i} : {coeff}")

    print(f"\n[ PHASE 3 ] SYMBOLIC OPTIMIZATION")
    print(f"  Searching for Vector Patterns: O2 (Origin²), D2 (Dir²), OD (Dot Product)")

    optimized_coeffs = [optimize_patterns(c) for c in poly.coefficients]  #
    for i, opt in enumerate(optimized_coeffs):
        print(f"    t^{i} : {opt}")

    print(f"\n[ PHASE 4 ] JIT COMPILATION : OPTIMIZED PYTHON CODE")
    print(f"  Generating kernel functions for real-time evaluation...")

    for i, opt in enumerate(optimized_coeffs):
        _, code = compile_dag_evaluator([opt], False)  #
        print(f"\n--- Kernel for t^{i} ---")
        indented_code = "    " + code.replace("\n", "\n    ")
        print(indented_code)

    print(f"\n" + "=" * 80)
    print(f"DAG COMPLEXITY ANALYSIS")
    print("=" * 80)

    order = topological_sort(implicit_function)
    print(f"  • Total unique operations in DAG : {len(order)}")
    print(f"  • Execution flow (Leaves to Root) :")

    for i, node in enumerate(order[:15]):
        print(f"    {i:03d} | {node}")
    if len(order) > 15:
        print(f"    ... and {len(order)-15} more operations.")

    print(f"\n[ SUCCESS ] Primitive '{surface_name}' is ready for the renderer.")
    print("=" * 80 + "\n")
