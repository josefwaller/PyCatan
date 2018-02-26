from pycatan.hex_type import HexType
from pycatan.point import Point

class Hex:
    def __init__(self, type, token_num, position, points):
        self.type = type
        self.token_num = token_num
        self.position = position
        self.points = points

    def __repr__(self):
        return "| %s, %s at r=%s, i=%s |" % (self.type, self.token_num, self.position[0], self.position[1])
