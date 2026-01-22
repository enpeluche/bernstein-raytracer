class Contact(object):
    __slots__ = ("t", "pt", "plan", "color")

    def __init__(self, t, pt, plan, color):
        self.t = t
        self.pt = pt
        self.plan = plan
        self.color = color
