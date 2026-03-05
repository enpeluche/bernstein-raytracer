from .variable import Variable

# Variables symboliques globales utilisées pour définir les surfaces.
# Elles servent de "clés" lors de la substitution ou de la conversion en polynômes.
x = Variable.make("x")
y = Variable.make("y")
z = Variable.make("z")


def plane_implicit_function():

    """
    Plan horizontal passant par l'origine (z = 0).
    """

    return z


def sphere_implicit_function():

    """
    Sphère unité centrée à l'origine (x² + y² + z² = 1).
    """

    return x ** 2 + y ** 2 + z ** 2 - 1.0


def paraboloid_implicit_function():

    """
    Paraboloïde de révolution (cuvette) orienté selon l'axe Z.
    Implicit equation : z = x² + y².
    """

    return x ** 2 + y ** 2 - z


def hyperbolic_paraboloid_implicit_function():

    """
    Selle de cheval (Paraboloïde hyperbolique).
    Implicit equation : z = x² - y².
    """

    return x ** 2 - y ** 2 - z


def cylinder_implicit_function():

    """
    Cylindre infini de rayon 1, centré sur l'axe Z.
    Implicit equation : x² + y² = 1.
    """

    return x ** 2 + y ** 2 - 1.0


def hyperbolic_cylinder_implicit_function():

    """
    Cylindre hyperbolique infini.
    Implicit equation : x² - y² = 1.
    """

    return x ** 2 - y ** 2 - 1.0


def parabolic_cylinder_implicit_function():

    """
    Cylindre parabolique (gouttière parabolique).
    Implicit equation : x² = -2y.
    """

    return x ** 2 + 2.0 * y


def elliptic_cone_implicit_function():

    """
    Cône elliptique parfait de sommet (0, 0, 0).
    Implicit equation : x² + y² = z².
    """

    return x ** 2 + y ** 2 - z ** 2


def steiner2_implicit_function():

    """
    Surface de Steiner (variante de degré 4).
    Implicit equation : x²y² - x²z² + y²z² - xyz = 0.
    """

    return x ** 2 * y ** 2 - x ** 2 * z ** 2 + y ** 2 * z ** 2 - x * y * z


def steiner4_implicit_function():

    """
    Surface de Steiner (forme développée de degré 4).
    Implicit equation complexe incluant un terme en z⁴.
    """

    return (
        y ** 2
        - 2.0 * x * y ** 2
        - x * z ** 2
        + x ** 2 * y ** 2
        + x ** 2 * z ** 2
        - z ** 4
    )


def hyperboloid_of_two_sheets_implicit_function():

    """
    Hyperboloïde à deux nappes (Sablier coupé).
    Implicit equation : x² + y² - z² + 0.1 = 0.
    """

    return x ** 2 + y ** 2 - z ** 2 + 0.1


def hyperboloid_of_one_sheet_implicit_function():

    """
    Hyperboloïde à une nappe (Sablier d'un seul bloc).
    Implicit equation : x² + y² - z² - 0.1 = 0.
    """

    return x ** 2 + y ** 2 - z ** 2 - 0.1


def roman_implicit_function():

    """
    Surface de Roman (variante de la surface de Steiner).
    Implicit equation : x²y² + x²z² + y²z² - 2xyz = 0.
    """

    return x ** 2 * y ** 2 + x ** 2 * z ** 2 + y ** 2 * z ** 2 - 2.0 * x * y * z


def torus_implicit_function(R=0.7, r=0.3):

    """
    Tore (Donut) de grand rayon R et de petit rayon r (tube).
    Implicit equation quartique développée pour éviter les racines carrées.
    """

    R2 = R * R
    r2 = r * r

    quadric = x ** 2 + y ** 2 + z ** 2 + R2 - r2

    return quadric ** 2 - 4.0 * R2 * (x ** 2 + y ** 2)


def cayley_implicit_function():

    """
    Surface cubique de Cayley (degré 3).
    Implicit equation : x² + y² + z² + x²z - y²z = 1.
    """

    return x ** 2 + y ** 2 + z ** 2 + x ** 2 * z - y ** 2 * z - 1.0


def whitney_umbrella_implicit_function():

    """
    Parapluie de Whitney (cubique).
    Implicit equation : x² - y²z = 0.
    """

    return x ** 2 - y ** 2 * z
