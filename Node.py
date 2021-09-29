class Node():
    def __init__(self, parent, pos):
        self.parent = parent
        self.pos = pos
        self.g_cost = 0
        self.h_cost = 0
        self.f_cost = 0

    def __eq__(self, o: object) -> bool:
        return o.pos == self.pos

    def getpos(self):
        return self.pos