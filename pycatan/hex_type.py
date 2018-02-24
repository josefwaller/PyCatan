from enum import Enum

# The different types of hexes available on a
# Catan board
class HexType(Enum):
    DESERT = 0
    FIELDS = 1
    PASTURE = 2
    MOUNTAINS = 3
    HILLS = 4
    FOREST = 5
