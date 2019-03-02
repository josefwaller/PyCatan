from enum import Enum
from pycatan.card import ResCard

# The different types of harbors found throughout the game
class HarborType(Enum):
    # the different 2:1 types
    Wood = 0
    Sheep = 1
    Brick = 2
    Wheat = 3
    Ore = 4

    # the 3:1 type
    Any = 5

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

        if self.type == HarborType.Wood:
            return "2:1W"

        elif self.type == HarborType.Sheep:
            return "2:1S"

        elif self.type == HarborType.Brick:
            return "2:1B"

        elif self.type == HarborType.Wheat:
            return "2:1Wh"

        elif self.type == HarborType.Ore:
            return "2:1O"

        elif self.type == HarborType.Any:
            return "3:1"

    @staticmethod
    def get_card_from_harbor_type(h_type):
        if h_type == HarborType.Wood:
            return ResCard.Wood
        elif h_type == HarborType.Brick:
            return ResCard.Brick
        elif h_type == HarborType.Wheat:
            return ResCard.Wheat
        elif h_type == HarborType.Ore:
            return ResCard.Ore
        elif h_type == HarborType.Sheep:
            return ResCard.Sheep
        elif h_type == HarborType.Any:
            return None
        else:
            raise Exception("Harbor has invalid type %s" % h_type)
