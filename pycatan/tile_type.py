from enum import Enum

# The different types of hexes available on a
# Catan board
class TileType(Enum):
    Desert = 0
    Fields = 1
    Pasture = 2
    Mountains = 3
    Hills = 4
    Forest = 5
