from enum import Enum

# The different types of harbors found throughout the game
class HarborType(Enum):
    # the different 2:1 types
    WOOD = 0
    SHEEP = 1
    BRICK = 2
    WHEAT = 3
    ORE = 4

    # the 3:1 type
    ANY = 5

# represents a catan harbor
class Harbor:

    def __init__(self, point_one, point_two, type):
        # sets the type
        self.type = type

        # sets the points
        self.point_one = point_one
        self.point_two = point_two

    def __repr__(self):
        return "Harbor %s, %s Type %s" % (self.point_one, self.point_two, self.type)

    def get_points(self):
        return [self.point_one, self.point_two]

    # returns a string representation of the type
    # Ex: 3:1, 2:1S, 2:1Wh
    def get_type(self):

        if self.type == HarborType.WOOD:
            return "2:1W"

        elif self.type == HarborType.SHEEP:
            return "2:1S"

        elif self.type == HarborType.BRICK:
            return "2:1B"

        elif self.type == HarborType.WHEAT:
            return "2:1Wh"

        elif self.type == HarborType.ORE:
            return "2:1O"

        elif self.type == HarborType.ANY:
            return "3:1"
