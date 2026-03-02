class Matrix:
    """
    Cette classe implémente les opérations matricielles de base (addition,
    soustraction, multiplication) avec des optimisations par déroulage de boucle
    (unrolling) pour les matrices 4x4 et les vecteurs colonnes 4x1.

    Elle est conçue pour fonctionner de pair avec la classe Transformation
    pour assurer le passage entre l'espace objet et l'espace monde.

    Attributes:
        mat (list[list[float]]): Les données brutes de la matrice.
        rows (int): Nombre de lignes.
        cols (int): Nombre de colonnes.
    """

    __slots__ = ("mat", "rows", "cols")

    def __init__(self, tab: list[list[float]]) -> None:
        """
        Créer un objet Matrix.

        Args:
            tab (list[list[float]])
        """
        self.mat = [[float(x) for x in row] for row in tab]
        self.rows = len(self.mat)
        self.cols = len(self.mat[0])

    def __getitem__(self, index: tuple[int, int]) -> float:
        """
        Args:
            index tuple[int, int]

        Returns:
            float
        """
        (i, j) = index
        return self.mat[i][j]

    def __add__(self, B: "Matrix") -> "Matrix":
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

    def __sub__(self, B: "Matrix") -> "Matrix":
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

    def __neg__(self) -> "Matrix":

        return Matrix(
            [[-self[i, j] for j in range(self.cols)] for i in range(self.rows)]
        )

    def __mul__(self, B: "Matrix") -> "Matrix":
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
            b = B.mat
            
            x = a[0][0]*b[0][0] + a[0][1]*b[1][0] + a[0][2]*b[2][0] + a[0][3]*b[3][0]
            y = a[1][0]*b[0][0] + a[1][1]*b[1][0] + a[1][2]*b[2][0] + a[1][3]*b[3][0]
            z = a[2][0]*b[0][0] + a[2][1]*b[1][0] + a[2][2]*b[2][0] + a[2][3]*b[3][0]
            w = a[3][0]*b[0][0] + a[3][1]*b[1][0] + a[3][2]*b[2][0] + a[3][3]*b[3][0]
            
            return Matrix([[x], [y], [z], [w]])

        # fmt: on

        for i in range(self.rows):
            for j in range(B.cols):
                for k in range(self.cols):
                    mul[i][j] += a[i][k] * b[k][j]

        return Matrix(mul)

    def __matmul__(self, B: "Matrix") -> "Matrix":
        return self.__mul__(B)

    def transpose(self) -> "Matrix":
        return Matrix(
            [[self[j, i] for j in range(self.rows)] for i in range(self.cols)]
        )

    def to_tuple(self) -> tuple[float]:
        """
        Transforme uen matrice avec une seule colonne en un tuple.
        """
        if self.cols != 1:
            raise ValueError(f"Le nombre de colonnes n'est pas égal à 1: c{self.cols}")

        return tuple(self[i, 0] for i in range(self.rows))

    def __str__(self):
        return "\n".join([str(row) for row in self.mat])
