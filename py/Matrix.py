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

        a = self.mat
        b = B.mat

        # fmt: off

        if B.rows == B.cols == self.rows == self.cols == 4:
            c00 = a[0][0] * b[0][0] + a[0][1] * b[1][0] + a[0][2] * b[2][0] + a[0][3] * b[3][0]
            c01 = a[0][0] * b[0][1] + a[0][1] * b[1][1] + a[0][2] * b[2][1] + a[0][3] * b[3][1]
            c02 = a[0][0] * b[0][2] + a[0][1] * b[1][2] + a[0][2] * b[2][2] + a[0][3] * b[3][2]
            c03 = a[0][0] * b[0][3] + a[0][1] * b[1][3] + a[0][2] * b[2][3] + a[0][3] * b[3][3]

            c10 = a[1][0] * b[0][0] + a[1][1] * b[1][0] + a[1][2] * b[2][0] + a[1][3] * b[3][0]
            c11 = a[1][0] * b[0][1] + a[1][1] * b[1][1] + a[1][2] * b[2][1] + a[1][3] * b[3][1]
            c12 = a[1][0] * b[0][2] + a[1][1] * b[1][2] + a[1][2] * b[2][2] + a[1][3] * b[3][2]
            c13 = a[1][0] * b[0][3] + a[1][1] * b[1][3] + a[1][2] * b[2][3] + a[1][3] * b[3][3]

            c20 = a[2][0] * b[0][0] + a[2][1] * b[1][0] + a[2][2] * b[2][0] + a[2][3] * b[3][0]
            c21 = a[2][0] * b[0][1] + a[2][1] * b[1][1] + a[2][2] * b[2][1] + a[2][3] * b[3][1]
            c22 = a[2][0] * b[0][2] + a[2][1] * b[1][2] + a[2][2] * b[2][2] + a[2][3] * b[3][2]
            c23 = a[2][0] * b[0][3] + a[2][1] * b[1][3] + a[2][2] * b[2][3] + a[2][3] * b[3][3]

            c30 = a[3][0] * b[0][0] + a[3][1] * b[1][0] + a[3][2] * b[2][0] + a[3][3] * b[3][0]
            c31 = a[3][0] * b[0][1] + a[3][1] * b[1][1] + a[3][2] * b[2][1] + a[3][3] * b[3][1]
            c32 = a[3][0] * b[0][2] + a[3][1] * b[1][2] + a[3][2] * b[2][2] + a[3][3] * b[3][2]
            c33 = a[3][0] * b[0][3] + a[3][1] * b[1][3] + a[3][2] * b[2][3] + a[3][3] * b[3][3]

            return Matrix([[c00,c01,c02,c03],
                           [c10,c11,c12,c13],
                           [c20,c21,c22,c23],
                           [c30,c31,c32,c33]])
        
        elif isinstance(B, Matrix) and B.cols == 1 and B.rows == 4:
            a = self.mat
            b = B.mat # b est une liste de listes [[x],[y],[z],[w]]
            
            # On écrit le produit Matrice * Vecteur en dur
            x = a[0][0]*b[0][0] + a[0][1]*b[1][0] + a[0][2]*b[2][0] + a[0][3]*b[3][0]
            y = a[1][0]*b[0][0] + a[1][1]*b[1][0] + a[1][2]*b[2][0] + a[1][3]*b[3][0]
            z = a[2][0]*b[0][0] + a[2][1]*b[1][0] + a[2][2]*b[2][0] + a[2][3]*b[3][0]
            w = a[3][0]*b[0][0] + a[3][1]*b[1][0] + a[3][2]*b[2][0] + a[3][3]*b[3][0]
            
            return Matrix([[x], [y], [z], [w]])

        # fmt: on

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

    def transpose(self):
        return Matrix(
            [[self[j, i] for j in range(self.rows)] for i in range(self.cols)]
        )

    def __str__(self):
        return "\n".join([str(row) for row in self.mat])
