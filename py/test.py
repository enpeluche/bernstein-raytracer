from sympy import symbols, expand, collect, cse


def generer_code_tore_raw():
    # 1. On définit les symboles BRUTS
    t, R, r = symbols("t R r")
    sx, sy, sz = symbols("sx sy sz")  # Origine
    dx, dy, dz = symbols("dx dy dz")  # Direction

    # 2. On construit le Rayon
    Rx = sx + t * dx
    Ry = sy + t * dy
    Rz = sz + t * dz

    # 3. L'équation du Tore (Aligné sur l'axe Y, couché au sol)
    # Distance au carré au centre
    dist_sq = Rx ** 2 + Ry ** 2 + Rz ** 2

    # Distance au carré à l'axe Y (le trou est vertical)
    dist_axis_sq = Rx ** 2 + Rz ** 2

    # Équation implicite
    terme_principal = (dist_sq + R ** 2 - r ** 2) ** 2
    terme_trou = 4 * R ** 2 * dist_axis_sq

    equation = terme_principal - terme_trou

    # 4. On développe et on trie
    print("Calcul symbolique en cours...")
    poly = collect(expand(equation), t)

    # 5. Extraction des coefficients
    coeffs = [
        poly.coeff(t, 4),  # A
        poly.coeff(t, 3),  # B
        poly.coeff(t, 2),  # C
        poly.coeff(t, 1),  # D
        poly.coeff(t, 0),  # E
    ]

    # 6. CSE : Optimisation
    replacements, resultats = cse(coeffs, symbols=symbols("x0:30"))

    # 7. Affichage
    print("-" * 50)
    print("   CODE OPTIMISÉ GÉNÉRÉ")
    print("-" * 50)

    print("# 1. Variables intermédiaires")
    for var_name, var_expr in replacements:
        print(f"{var_name} = {var_expr}")

    print("\n# 2. Coefficients du polynôme")
    noms = ["A", "B", "C", "D", "E"]

    # --- LA CORRECTION EST ICI (plus de [0]) ---
    for nom, res in zip(noms, resultats):
        print(f"{nom} = {res}")
    print("-" * 50)


if __name__ == "__main__":
    generer_code_tore_raw()
