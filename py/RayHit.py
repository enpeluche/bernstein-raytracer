from Matrix import Matrix


class RayHit:
    """ """

    __slots__ = ("t", "pt", "plan", "color")

    def __init__(self, t, pt, plan, color):
        """

        :param t: Description
        :param pt: Description
        :param plan: Description
        :param color: Description
        """
        self.t = t
        self.pt = pt
        self.plan = plan
        self.color = color

    def transform(self, T):
        (x, y, z) = self.pt
        vpt = (x, y, z, 1)
        [a, b, c, d] = self.plan
        vplan = [a, b, c, d]

        matvpt = Matrix(vpt)
        matvplan = Matrix(vplan)

        transfomatvpt = T.forward * matvpt
        transfomatvplan = T.backward * matvplan

        trf_pt = (
            transfomatvpt.get(0, 0),
            transfomatvpt.get(0, 1),
            transfomatvpt.get(0, 2),
        )
        trf_contact = (
            transfomatvplan.get(0, 0),
            transfomatvplan.get(0, 1),
            transfomatvplan.get(0, 2),
            transfomatvplan.get(0, 3),
        )
        return Contact(contact.t, trf_pt, trf_plan, contact.color)
