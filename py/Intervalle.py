class Intervalle:
    """
    Représente un segment 1D le long d'un rayon (raytracing).
    Dans le contexte de la géométrie de construction de solides (CSG),
    un intervalle définit la portion du rayon qui se trouve "à l'intérieur" d'un objet.
    """

    __slots__ = ("a", "b")

    def __init__(self, a, b):
        """
        Initialise un nouvel intervalle.

        Args:
            a (RayHit): Le point d'entrée du rayon dans la matière (borne inférieure).
            b (RayHit): Le point de sortie du rayon de la matière (borne supérieure).
        """
        self.a = a
        self.b = b

    def __repr__(self):
        """Représentation textuelle de l'intervalle pour le débogage."""
        return f"[{self.a}, {self.b}]"
