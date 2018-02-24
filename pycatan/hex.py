from pycatan.hex_type import HexType
from pycatan.point import Point

class Hex:
    def __init__(self, type, token_num, points):
        self.type = type
        self.token_num = token_num
        self.points = points

    def __repr__(self):
        return "| %s, %s |" % (self.type, self.token_num)
