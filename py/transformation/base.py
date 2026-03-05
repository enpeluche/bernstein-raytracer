from Matrix import Matrix


class Transformation:
    """
    Représente une transformation de l'espace dans le groupe affine Aff(3).

    Cette classe manipule des matrices de passage 4x4 en coordonnées homogènes,
    permettant de combiner rotations, translations et homothéties.
    Elle stocke la transformation directe et son inverse pour optimiser les calculs.
    """

    __slots__ = ("forward", "backward")

    def __init__(
        self, forward: Matrix | tuple[tuple], backward: Matrix | tuple[tuple]
    ) -> None:
        """
        Args:
            forward (Matrix or tuple[tuple]): La matrice de la transformation (doit être inversible).
            backward (Matrix or tuple[tuple]): La matrice inverse pré-calculée de 'forward'.
        """
        self.forward = forward if isinstance(forward, Matrix) else Matrix(forward)
        self.backward = backward if isinstance(backward, Matrix) else Matrix(backward)

    def __mul__(self, a: "Transformation") -> "Transformation":
        """
        Surcharge de l'opérateur *.
        Renvoie la transformation résultante d'effectuer la transformation a puis la transformation self.

        Args:
            a (Transformation)
        """
        return Transformation(self.forward * a.forward, a.backward * self.backward)

    def __invert__(self) -> "Transformation":
        """
        Surcharge de l'opérateur ~.
        Retourne sa transformation inverse.
        """
        return Transformation(self.backward, self.forward)
