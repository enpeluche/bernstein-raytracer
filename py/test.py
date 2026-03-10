from DAG import *
from Polynomial import *
from DAG.compiler import optimize_patterns, topological_sort, generate_python_function

x, y, z = Variable.make("x"), Variable.make("y"), Variable.make("z")

ox, oy, oz = Variable.make("ox"), Variable.make("oy"), Variable.make("oz")
dx, dy, dz = Variable.make("dx"), Variable.make("dy"), Variable.make("dz")

env = {
    "x": Polynomial([ox, dx]),
    "y": Polynomial([oy, dy]),
    "z": Polynomial([oz, dz]),
}
if __name__ == "__main__":

    R = 0.7
    r = 0.3
    R2 = R * R
    r2 = r * r

    quadric = x ** 2 + y ** 2 + z ** 2 + R2 - r2

    surface_name = "torus"
    surface_eq = quadric ** 2 - 4.0 * R2 * (x ** 2 + y ** 2)

    RAY_PROTOCOL = ["ox", "oy", "oz", "dx", "dy", "dz", "O2", "D2", "OD"]
    POINT_PROTOCOL = ["x", "y", "z"]

    print("=" * 80)
    print(f"COMPILER SUITE: ANALYZING {surface_name}")
    print("=" * 80)

    # symbolic analysis
    print(f"\n[ PHASE 1 ] SYMBOLIC GEOMETRY")
    print(f"  • Implicit Equation : f(x, y, z) = {surface_eq}")

    dfx = surface_eq.partial_derivative("x")
    dfy = surface_eq.partial_derivative("y")
    dfz = surface_eq.partial_derivative("z")

    print(f"  • Gradient ∇f (Normal vectors) :")
    print(f"    ∂f/∂x : {dfx}")
    print(f"    ∂f/∂y : {dfy}")
    print(f"    ∂f/∂z : {dfz}")

    print(f"  • Gradient ∇f (Normal vectors) :")
    _, code_dfx = generate_python_function(dfx)
    _, code_dfy = generate_python_function(dfy)
    _, code_dfz = generate_python_function(dfz)
    print(f"    ∂f/∂x : {code_dfx}")
    print(f"    ∂f/∂y : {code_dfy}")
    print(f"    ∂f/∂z : {code_dfz}")

    # ray injection
    print(f"\n[ PHASE 2 ] RAY PARAMETERIZATION")
    print(f"  Substituting: P(t) = O + tD")
    print(f"  (x, y, z) ➔ (ox + t*dx, oy + t*dy, oz + t*dz)")

    poly = surface_eq.to_polynomial(env)
    print(f"\n  Resulting Polynomial P(t) coefficients (Raw):")
    for i, coeff in enumerate(poly.coefficients):
        print(f"    t^{i} : {coeff}")

    # optimize patterns
    print(f"\n[ PHASE 3 ] SYMBOLIC OPTIMIZATION")
    print(f"  Searching for Vector Patterns: O2 (Origin²), D2 (Dir²), OD (Dot Product)")

    optimized_coeffs = [optimize_patterns(c) for c in poly.coefficients]
    for i, opt in enumerate(optimized_coeffs):
        print(f"    t^{i} : {opt}")

    # jit compilation
    print(f"\n[ PHASE 4 ] JIT COMPILATION : OPTIMIZED PYTHON CODE")
    print(f"  Generating kernel functions for real-time evaluation...")

    for i, opt in enumerate(optimized_coeffs):
        _, code = generate_python_function(opt, RAY_PROTOCOL)
        print(f"\n--- Kernel for t^{i} ---")
        indented_code = "  " + code.replace("\n", "\n  ")
        print(indented_code)

    # dag topology
    print(f"\n" + "=" * 80)
    print(f"DAG COMPLEXITY ANALYSIS")
    print("=" * 80)

    order = topological_sort(surface_eq)
    print(f"  • Total unique operations in DAG : {len(order)}")
    print(f"  • Execution flow (Leaves to Root) :")

    for i, node in enumerate(order[:15]):
        print(f"    {i:03d} | {node}")
    if len(order) > 15:
        print(f"    ... and {len(order)-15} more operations.")

    print(f"\n[ SUCCESS ] Primitive '{surface_name}' is ready for the renderer.")
    print("=" * 80 + "\n")
