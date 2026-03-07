from .number import Number
from .variable import Variable
from .plus import Plus
from .mult import Mult
from .opp import Opp
from .pow import Pow


def topo_sort(root):
    """
    Perform a topological sort on the DAG starting from a root node.

    This function flattens the recursive structure of the expression graph into
    a linear list. It ensures that every node appears in the list only after
    all of its dependencies (children) have been processed. This is the
    foundational step for code generation and Common Subexpression Elimination (CSE).

    Args:
        root (DAG): The terminal node of the mathematical expression.

    Returns:
        list[DAG]: A list of nodes in post-order (leaves first, root last).
    """

    visited = set()
    order = []

    def dfs(node):

        if node in visited:
            return

        visited.add(node)

        for a in node.args:
            dfs(a)

        order.append(node)

    dfs(root)

    return order


def _generate_python_function(root):

    nodes = topo_sort(root)

    index = {node: i for i, node in enumerate(nodes)}

    lines = []
    lines.append("def compiled(env):")

    indent = "    "

    for node in nodes:

        i = index[node]

        if isinstance(node, Number):

            lines.append(f"{indent}t{i} = {node.value}")

        elif isinstance(node, Variable):

            lines.append(f"{indent}t{i} = env['{node.name}']")

        elif isinstance(node, Plus):

            args = [f"t{index[a]}" for a in node.args]
            expr = " + ".join(args)

            lines.append(f"{indent}t{i} = {expr}")

        elif isinstance(node, Mult):

            args = [f"t{index[a]}" for a in node.args]
            expr = " * ".join(args)

            lines.append(f"{indent}t{i} = {expr}")

        elif isinstance(node, Pow):

            base = f"t{index[node.base]}"

            lines.append(f"{indent}t{i} = {base} ** {node.exp}")

    lines.append(f"{indent}return t{index[root]}")

    code = "\n".join(lines)

    namespace = {}

    exec(code, namespace)

    return namespace["compiled"], code


def generate_python_function(root):
    nodes = topo_sort(root)
    index = {node: i for i, node in enumerate(nodes)}

    # Dans generate_python_function
    vars_needed = sorted(list(set(n.name for n in nodes if isinstance(n, Variable))))
    vars_needed.append("**env")  # On ajoute ça pour la compatibilité
    args_str = ", ".join(vars_needed)

    lines = [f"def compiled({args_str}):"]

    indent = "    "

    for node in nodes:
        i = index[node]

        if isinstance(node, Number):
            lines.append(f"{indent}t{i} = {node.value}")

        elif isinstance(node, Variable):
            # Plus de dictionnaire ! On utilise l'argument direct
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

        # --- LE FIX : Gestion de l'opposition (négatif) ---
        elif hasattr(node, "__class__") and node.__class__.__name__ == "Opp":
            arg = f"t{index[node.args[0]]}"
            lines.append(f"{indent}t{i} = -{arg}")

        # --- SÉCURITÉ : Ne rien laisser passer ---
        else:
            # Si on tombe ici, c'est qu'un nouveau type de nœud n'est pas géré
            lines.append(f"{indent}t{i} = # ERROR: Unknown node type {type(node)}")

    lines.append(f"{indent}return t{index[root]}")

    code = "\n".join(lines)
    namespace = {}
    try:
        exec(code, namespace)
    except Exception as e:
        print(f"Compilation Error: {e}\nCode generated:\n{code}")

    return namespace["compiled"], code


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


def compile(self):

    from .compiler import generate_python_function

    return generate_python_function(self)


def topo_sort_multiple(roots):
    """Effectue un tri topologique sur une forêt de DAGs."""
    visited = set()
    order = []

    def dfs(node):
        if node in visited:
            return
        visited.add(node)
        # On visite les enfants (dépendances)
        for a in getattr(node, "args", []):  # Gère Number/Variable qui n'ont pas d'args
            dfs(a)
        order.append(node)

    for r in roots:
        dfs(r)
    return order


def generate_python_poly_function(roots, is_spatial):

    # union des DAGs
    all_nodes = set()
    for r in roots:
        all_nodes.update(topo_sort(r))

    nodes = topo_sort_multiple(roots)  # ou un topo_sort sur le DAG fusionné
    index = {node: i for i, node in enumerate(nodes)}

    if is_spatial:
        args_str = "x, y, z, **env"
    else:
        vars_needed = sorted(set(n.name for n in nodes if isinstance(n, Variable)))
        vars_needed.append("**env")
        args_str = ", ".join(vars_needed)

    lines = [f"def compiled_poly({args_str}):"]
    indent = "    "

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

        elif node.__class__.__name__ == "Opp":
            arg = f"t{index[node.args[0]]}"
            lines.append(f"{indent}t{i} = -{arg}")

        else:
            raise TypeError(f"Unknown node type {type(node)}")

    # retour des coefficients
    outputs = ", ".join(f"t{index[r]}" for r in roots)
    lines.append(f"{indent}return [{outputs}]")

    code = "\n".join(lines)
    namespace = {}
    exec(code, namespace)

    return namespace["compiled_poly"], code


def analyze_primitive_compiler(implicit_function, surface_name, env):
    """
    Exécute une suite complète d'analyses et de logs pour une surface implicite
    pendant la phase de compilation JIT.
    """
    print("=" * 80)
    print(f"COMPILER SUITE: ANALYZING {surface_name}")
    print("=" * 80)

    # PHASE 1 : Géométrie Symbolique
    print(f"\n[ PHASE 1 ] SYMBOLIC GEOMETRY")
    print(f"  • Implicit Equation : f(x, y, z) = {implicit_function}")

    dfx = implicit_function.partial_derivative("x")
    dfy = implicit_function.partial_derivative("y")
    dfz = implicit_function.partial_derivative("z")

    print(f"  • Gradient ∇f (Normal vectors) :")
    print(f"    ∂f/∂x : {dfx}")
    print(f"    ∂f/∂y : {dfy}")
    print(f"    ∂f/∂z : {dfz}")

    # PHASE 2 : Paramétrisation du Rayon
    print(f"\n[ PHASE 2 ] RAY PARAMETERIZATION")
    print(f"  Substituting: P(t) = O + tD")
    print(f"  (x, y, z) ➔ (ox + t*dx, oy + t*dy, oz + t*dz)")

    # Conversion en polynôme de t selon l'environnement défini dans primitive.py
    poly = implicit_function.to_polynomial(env)  #
    print(f"\n  Resulting Polynomial P(t) coefficients (Raw):")
    for i, coeff in enumerate(poly.coefficients):
        print(f"    t^{i} : {coeff}")

    # PHASE 3 : Optimisation Symbolique
    print(f"\n[ PHASE 3 ] SYMBOLIC OPTIMIZATION")
    print(f"  Searching for Vector Patterns: O2 (Origin²), D2 (Dir²), OD (Dot Product)")

    optimized_coeffs = [optimize_patterns(c) for c in poly.coefficients]  #
    for i, opt in enumerate(optimized_coeffs):
        print(f"    t^{i} : {opt}")

    # PHASE 4 : Compilation JIT
    print(f"\n[ PHASE 4 ] JIT COMPILATION : OPTIMIZED PYTHON CODE")
    print(f"  Generating kernel functions for real-time evaluation...")

    for i, opt in enumerate(optimized_coeffs):
        # Utilisation de ta fonction de génération de code
        _, code = generate_python_poly_function([opt], False)  #
        print(f"\n--- Kernel for t^{i} ---")
        indented_code = "    " + code.replace("\n", "\n    ")
        print(indented_code)

    # ANALYSE DE COMPLEXITÉ DU DAG
    print(f"\n" + "=" * 80)
    print(f"DAG COMPLEXITY ANALYSIS")
    print("=" * 80)

    # Tri topologique pour analyser le graphe d'exécution
    from DAG.compiler import topo_sort  #

    order = topo_sort(implicit_function)
    print(f"  • Total unique operations in DAG : {len(order)}")
    print(f"  • Execution flow (Leaves to Root) :")

    for i, node in enumerate(order[:15]):
        print(f"    {i:03d} | {node}")
    if len(order) > 15:
        print(f"    ... and {len(order)-15} more operations.")

    print(f"\n[ SUCCESS ] Primitive '{surface_name}' is ready for the renderer.")
    print("=" * 80 + "\n")
