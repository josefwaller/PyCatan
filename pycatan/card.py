from enum import Enum

# The different types of resource cards
class ResCard(Enum):

    # the resource cards
    Wood = 0
    Brick = 1
    Ore = 2
    Sheep = 3
    Wheat = 4

# The different types of developement cards
class DevCard(Enum):

    # the developement cards
    Road = 0
    VictoryPoint = 1
    Knight = 2
    Monopoly = 3
    YearOfPlenty = 4
