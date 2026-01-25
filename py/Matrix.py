from util import *

# point 4H:[[x], [y], [z], [1]]
# vecteur 4H:[[x], [y], [z], [0]]


class Matrix:
    """ """

    def __init__(self, tab):
        """
        Créer un objet Matrix.

        Args:
            tab (list[list[float]])
        """
        self.mat = tab
        self.rows = len(tab)
        self.cols = len(tab[0])

    def __getitem__(self, index):
        """
        Args:
            index tuple[int, int]
        """
        (i, j) = index
        return self.mat[i][j]

    def __add__(self, B):
        """
        Args:
            B (Matrix)
        """

        if self.cols != B.cols or self.rows != B.rows:
            raise ValueError(
                f"Dimensions incompatibles: (r:{self.rows},c:{self.cols}) contre (r:{B.rows},c:{B.cols})"
            )

        return Matrix(
            [[self[i, j] + B[i, j] for j in range(self.cols)] for i in range(self.rows)]
        )

    def __sub__(self, B):
        """
        Args:
            B (Matrix)
        """

        if self.cols != B.cols or self.rows != B.rows:
            raise ValueError(
                f"Dimensions incompatibles: (r:{self.rows},c:{self.cols}) contre (r:{B.rows},c:{B.cols})"
            )

        return Matrix(
            [[self[i, j] - B[i, j] for j in range(self.cols)] for i in range(self.rows)]
        )

    def __neg__(self):

        return Matrix(
            [[-self[i, j] for j in range(self.cols)] for i in range(self.rows)]
        )

    def __mul__(self, B):
        """
        Args:
            B (Matrix)
        """

        if self.cols != B.rows:
            raise ValueError(
                f"Dimensions incompatibles: (c:{self.cols}) contre (r:{B.rows})"
            )

        mul = [[0.0] * B.cols for _ in range(self.rows)]

        for i in range(self.rows):
            for j in range(B.cols):
                for k in range(self.cols):
                    mul[i][j] += self[i, k] * B[k, j]

        return Matrix(mul)

    def to_tuple(self):
        """
        Transforme uen matrice avec une seule colonne en un tuple.
        """
        if self.cols != 1:
            raise ValueError(f"Le nombre de colonnes n'est pas égal à 1: c{self.cols}")

        return tuple(self[i, 0] for i in range(self.rows))

    def __str__(self):
        return "\n".join([str(row) for row in self.mat])
