class Intervalle:
    """ """

    __slots__ = ("a", "b")

    def __init__(self, a, b):
        """
        Docstring for __init__

            a (RayHit):
            b (RayHit):
        """
        self.a = a
        self.b = b

    def __repr__(self):
        return f"[{self.a}, {self.b}]"
