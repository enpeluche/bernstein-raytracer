from RayHit import RayHit


class Interval:
    """
    Représente un segment 1D le long d'un rayon (raytracing).
    Dans le contexte de la géométrie de construction de solides (CSG),
    un intervalle définit la portion du rayon qui se trouve "à l'intérieur" d'un objet.
    """

    __slots__ = ("hit_in", "hit_out")

    def __init__(self, hit_in: RayHit, hit_out: RayHit) -> None:
        """
        Initialise un nouvel intervalle.

        Args:
            hit_in (RayHit): Le point d'entrée du rayon dans la matière (borne inférieure).
            hit_out (RayHit): Le point de sortie du rayon de la matière (borne supérieure).
        """
        self.hit_in = hit_in
        self.hit_out = hit_out

    def __repr__(self):
        """Représentation textuelle de l'intervalle pour le débogage."""
        return f"[{self.hit_in}, {self.hit_out}]"
