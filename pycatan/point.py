class Point:
    def __init__(self, hexes, position):
        self.hexes = hexes
        self.building = None
        self.position = position

    def __repr__(self):
        return "| Point at r=%s, i=%s |" % (self.position[0], self.position[1])
