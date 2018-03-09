from pycatan.board import Board
from pycatan.hex import Hex
from pycatan.point import Point
from pycatan.hex_type import HexType
from pycatan.harbor import Harbor, HarborType

import math
import random

# The default, hexagonal board filled with random hexes and tokens
class DefaultBoard(Board):

    def __init__(self, game):
        super(DefaultBoard, self).__init__(game)

        # Set hexes
        hex_deck = Board.get_shuffled_hex_deck()
        token_deck = Board.get_shuffled_hex_nums()
        temp_hexes = []
        for r in range(5):
            temp_hexes.append([])
            for i in range([3, 4, 5, 4, 3][r]):
                # Add a hex
                new_hex = Hex(type=hex_deck.pop(), token_num=None, position=[r, i], points=[])
                temp_hexes[-1].append(new_hex)
                # Remove the token if it is the desert
                if new_hex.type == HexType.DESERT:
                    self.robber = [r, i]
                else:
                    new_hex.token_num = token_deck.pop()

        self.hexes = tuple(map(lambda x: tuple(x), temp_hexes))

        # Add points
        temp_points = []
        for r in range(6):
            temp_points.append([])
            for i in range([7, 9, 11, 11, 9, 7][r]):
                point = Point(hexes=[], position=[r, i])
                temp_points[-1].append(point)
                # Set point/hex relations
                for pos in DefaultBoard.get_hex_indexes_for_point(r, i):
                    point.hexes.append(self.hexes[pos[0]][pos[1]])
                    self.hexes[pos[0]][pos[1]].points.append(point)


        self.points = tuple(map(lambda x: tuple(x), temp_points))
        # Set the connected points for each point
        # Must be done after initializing each point so that the point object exists
        for r in self.points:
            for p in r:
                p.connected_points = self.get_connected_points(p.position[0], p.position[1])
        # adds a harbor for each points in the pattern 2 3 2 2 3 2 etc
        outside_points = DefaultBoard.get_outside_points()
        # the pattern of spaces between harbors
        pattern = [1, 2, 1]
        # the current index of pattern
        index = 0
        # the different types of harbors
        harbor_types = [
            HarborType.WOOD,
            HarborType.BRICK,
            HarborType.ORE,
            HarborType.WHEAT,
            HarborType.SHEEP,
            HarborType.ANY,
            HarborType.ANY,
            HarborType.ANY,
            HarborType.ANY
        ]
        # Shuffles the harbors
        random.shuffle(harbor_types)
        # Run loop until harbor_types is empty
        while harbor_types:
            # Create a new harbor
            p_one = outside_points.pop()
            p_two = outside_points.pop()
            harbor = Harbor(
                point_one = self.points[p_one[0]][p_one[1]],
                point_two = self.points[p_two[0]][p_two[1]],
                type = harbor_types.pop())
            # Add it to harbors
            self.harbors.append(harbor)
            # Remove the unused points from outside_points
            for _ in range(pattern[index % len(pattern)]):
                outside_points.pop()
            # Use next pattern value for number of points inbetween next time
            index += 1

        # puts the robber on the desert hex to start
        for r in range(len(temp_hexes)):
            # checks if this row has the desert
            if temp_hexes[r].count(HexType.DESERT) > 0:
                # places the robber
                self.robber = [r, temp_hexes[r].index(HexType.DESERT)]

    # Returns the indexes of the hexes connected to a certain points
    # on the default, hexagonal Catan board
    @staticmethod
    def get_hex_indexes_for_point(r, i):
        # the indexes of the hexes
        hex_indexes = []
        # Points on a hexagonal board
        points = [
            [None] * 7,
            [None] * 9,
            [None] * 11,
            [None] * 11,
            [None] * 9,
            [None] * 7
        ]
        # gets the adjacent hexes differently depending on whether the point is in the top or the bottom
        if r < len(points) / 2:
            # gets the hexes below the point ------------------

            # adds the hexes to the right
            if i < len(points[r]) - 1:
                hex_indexes.append([r, math.floor(i / 2)])

            # if the index is even, the number is between two hexes
            if i % 2 == 0 and i > 0:
                hex_indexes.append([r, math.floor(i / 2) - 1])

            # gets the hexes above the point ------------------

            if r > 0:
                # gets the hex to the right
                if i > 0 and i < len(points[r]) - 2:
                    hex_indexes.append([r - 1, math.floor((i - 1) / 2)])

                # gets the hex to the left
                if i % 2 == 1 and i < len(points[r]) - 1 and i > 1:
                    hex_indexes.append([r - 1, math.floor((i - 1) / 2) - 1])

        else:

            # adds the below -------------

            if r < len(points) - 1:
                # gets the hex to the right or directly below
                if i < len(points[r]) - 2 and i > 0:
                    hex_indexes.append([r, math.floor((i - 1) / 2)])

                # gets the hex to the left
                if i % 2 == 1 and i > 1 and i < len(points[r]):
                    hex_indexes.append([r, math.floor((i - 1) / 2 - 1)])

            # gets the hexes above ------------

            # gets the hex above and to the right or directly above
            if i < len(points[r]) - 1:
                hex_indexes.append([r - 1, math.floor(i / 2)])

            # gets the hex to the left
            if i > 1 and i % 2 == 0:
                hex_indexes.append([r - 1, math.floor((i - 1) / 2)])

        return hex_indexes

    # gets the points that are connected to the point given
    def get_connected_points(self, r, i):
        to_return = []
        # Get the point to the left and the right
        if i > 0:
            to_return.append(self.points[r][i - 1])

        if i < len(self.points[r]) - 1:
            to_return.append(self.points[r][i + 1])

        # Get the point above and below
        # First, if the point is in the center two rows, the connected point
        # is either directly above/below this point
        if r == 2 and i % 2 == 0:
            to_return.append(self.points[r + 1][i])
        elif r == 3 and i % 2 == 0:
            to_return.append(self.points[r - 1][i])
        # If the point is not in the 2 center rows, the point will have an offset
        elif r < len(self.points) / 2:
            if i % 2 == 0:
                to_return.append(self.points[r + 1][i + 1])
            elif r > 0 and i > 0:
                to_return.append(self.points[r - 1][i - 1])
        else:
            if i % 2 == 0:
                to_return.append(self.points[r - 1][i + 1])
            elif r < len(self.points) - 1 and i > 0:
                to_return.append(self.points[r + 1][i - 1])
        return to_return

    # Get the points along the outside of the board, in clockwise order
    @staticmethod
    def get_outside_points():
        # The lengths of each row of points on the board
        row_lengths = [
            7,
            9,
            11,
            11,
            9,
            7
        ]
        # The points on the bottom
        bottom = list(map(lambda x: [len(row_lengths) - 1, x], range(row_lengths[-1])))
        # The points on the top
        top = list(map(lambda x: [0, x], range(row_lengths[0])))
        # adds all the points on the right and left
        right = []
        left = []
        for r in range(1, len(row_lengths) - 1):
            # Get the last two and first two points on this row
            last_two = list(map(lambda x: [r, x], range(row_lengths[r])[-2:]))
            first_two = list(map(lambda x: [r, x], reversed(range(2))))
            # If the points are one the bottom half of the board, reverse them
            if r > (len(row_lengths) - 1) / 2:
                last_two = list(reversed(last_two))
                first_two = list(reversed(first_two))
            # Add points to right and left
            right.extend(last_two)
            left.extend(first_two)

        # Put different sides of points in order
        # bottom and left are reversed since we want to count those points in reverse order
        # to make sure we go in clockwise order
        outside_points = []
        outside_points.extend(top)
        outside_points.extend(right)
        outside_points.extend(reversed(bottom))
        outside_points.extend(reversed(left))
        # Return them
        return outside_points
