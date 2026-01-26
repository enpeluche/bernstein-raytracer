from DAG import *

x = Var("x")
y = Var("y")
z = Var("z")


class Steiner2DAG(M):
    def __init__(self):
        self.expr = x * x * y * y - x * x * z * z + y * y * z * z - x * y * z

    def to_poly(self, dico):
        return self.expr.to_poly(dico)

    def derivee(self, nom):
        return self.expr.derivee(nom)


class Steiner4DAG(M):
    def __init__(self):
        self.expr = (
            y * y
            - Nb(2.0) * x * y * y
            - x * z * z
            + x * x * y * y
            + x * x * z * z
            - z * z * z * z
        )

    def to_poly(self, dico):
        return self.expr.to_poly(dico)

    def derivee(self, nom):
        return self.expr.derivee(nom)


class HyperboloidTwoSheetsDAG(M):
    def __init__(self):
        self.expr = Nb(0.0) - (z * z - (x * x + y * y + Nb(0.1)))

    def to_poly(self, dico):
        return self.expr.to_poly(dico)

    def derivee(self, nom):
        return self.expr.derivee(nom)


class HyperboloidOneSheetDAG(M):
    def __init__(self):
        self.expr = Nb(0.0) - (z * z - (x * x + y * y - Nb(0.1)))

    def to_poly(self, dico):
        return self.expr.to_poly(dico)

    def derivee(self, nom):
        return self.expr.derivee(nom)


class RomanDAG(M):
    def __init__(self):
        self.expr = x * x * y * y + x * x * z * z + y * y * z * z - Nb(2.0) * x * y * z

    def to_poly(self, dico):
        return self.expr.to_poly(dico)

    def derivee(self, nom):
        if nom == "x":
            return Nb(2.0) * x * y * y + Nb(2.0) * x * z * z - Nb(2.0) * y * z

        elif nom == "y":
            return Nb(2.0) * y * x * x + Nb(2.0) * y * z * z - Nb(2.0) * x * z

        elif nom == "z":
            return Nb(2.0) * z * x * x + Nb(2.0) * z * y * y - Nb(2.0) * x * y

        else:
            return Nb(0.0)


# fmt: off
#
# Avant, on avait ça et c'était plus lent car le solveur devait tout redécouvrir.
#
#return ((x-Nb(cx))*(x-Nb(cx))+(y-Nb(cy))*(y-Nb(cy))+(z-Nb(cz))*(z-Nb(cz))-Nb(r)*Nb(r)
#
#fmt : on

class SphereDAG(M):
    __slots__ = ("r2")

    def __init__(self, r):
        self.r2 = float(r * r)

    def to_poly(self, dico):
        """
        Surcharge de la méthode to_poly

        :param self: Description
        :param dico: Description
        """
        px = dico["x"].c
        py = dico["y"].c
        pz = dico["z"].c

        sx = px[0]
        dx = px[1] if len(px) > 1 else 0.0

        sy = py[0]
        dy = py[1] if len(py) > 1 else 0.0

        sz = pz[0]
        dz = pz[1] if len(pz) > 1 else 0.0

        a = dx * dx + dy * dy + dz * dz
        b = 2.0 * (sx * dx + sy * dy + sz * dz)
        c = (sx * sx + sy * sy + sz * sz) - self.r2

        return Polynome([c, b, a])

    def derivee(self, nom):
        if nom == "x":
            return Mult(Nb(2.0), Var("x"))

        elif nom == "y":
            return Mult(Nb(2.0), Var("y"))

        elif nom == "z":
            return Mult(Nb(2.0), Var("z"))

        else:
            return Nb(0.0)


class ToreDAG(M):
    __slots__ = ("r2", "R2")

    def __init__(self, r, R):
        self.r2 = float(r * r)
        self.R2 = float(R * R)

    def to_poly(self, dico):

        """
        Surcharge de la méthode to_poly
        
        :param self: Description
        :param dico: Description
        """

        px = dico["x"].c
        py = dico["y"].c
        pz = dico["z"].c

        sx = px[0]
        dx = px[1] if len(px) > 1 else 0.0

        sy = py[0]
        dy = py[1] if len(py) > 1 else 0.0

        sz = pz[0]
        dz = pz[1] if len(pz) > 1 else 0.0

        R2 = self.R2
        r2 = self.r2

        dx2 = dx * dx
        dy2 = dy * dy
        dz2 = dz * dz

        sx2 = sx * sx
        sy2 = sy * sy
        sz2 = sz * sz

        sdx = sx * dx
        sdy = sy * dy
        sdz = sz * dz

        DD = dx2 + dy2 + dz2

        SS = sx2 + sy2 + sz2

        SD = sdx + sdy + sdz

        axz = dx2 + dz2
        bxz = sdx + sdz
        cxz = sx2 + sz2

        K = SS + R2 - r2
        FourR2 = 4.0 * R2

        A = DD * DD

        B = 4.0 * DD * SD

        C = 2.0 * DD * K + 4.0 * SD * SD - FourR2 * axz

        D = 4.0 * SD * K - 2.0 * FourR2 * bxz

        E = K * K - FourR2 * cxz

        return Polynome([E, D, C, B, A])

    def derivee(self, nom):

        R2 = self.R2
        r2 = self.r2

        const_xz = -(R2 + r2)
        const_y = R2 - r2

        x_sq = Mult(Var("x"), Var("x"))
        y_sq = Mult(Var("y"), Var("y"))
        z_sq = Mult(Var("z"), Var("z"))

        sum_sq = Plus(x_sq, Plus(y_sq, z_sq))

        if nom == "x":
            terme_parenthese = Plus(sum_sq, Nb(const_xz))
            return Mult(Mult(Nb(4.0), Var("x")), terme_parenthese)

        elif nom == "z":
            terme_parenthese = Plus(sum_sq, Nb(const_xz))
            return Mult(Mult(Nb(4.0), Var("z")), terme_parenthese)

        elif nom == "y":
            terme_parenthese = Plus(sum_sq, Nb(const_y))
            return Mult(Mult(Nb(4.0), Var("y")), terme_parenthese)

        else:
            return Nb(0.0)
