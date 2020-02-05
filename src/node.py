class Node():

    def __init__(self, x, y, walkable = True):
        self.x = x
        self.y = y
        self.walkable = walkable
        self.f = 0
        self.g = 0
        self.h = 0
        self.opened = False
        self.closed = False
        self.parent = None

    def __lt__(self, other):
        return self.g - self.f < other.g - other.f

    def __gt__(self, other):
        return self.g - self.f > other.g - other.f