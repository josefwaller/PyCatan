from pycatan.harbor import Harbor, HarborType
from pycatan.player import Player
from pycatan.statuses import Statuses
from pycatan.building import Building
from pycatan.hex_type import HexType
from pycatan.card import ResCard, DevCard
from pycatan.hex import Hex
from pycatan.point import Point

# used to shuffle the deck of hexes
import random

# used for lots of things
import math

# used for reading the starting_board file
import json

# used for debugging
import pprint

class Board:

    def __init__(self, game, starting_board=False):
        # the game the board is in
        self.game = game
        # the hexes on the board
        self.hexes = []
        # the points on the board
        # where the players can place settlements/cities
        self.points = []
        # the roads
        self.roads = []
        # all of the circular number tokens in the game
        self.all_hex_nums = []
        # the locations of the harbors
        self.harbors = []
        # the location of the robber
        # going r, i
        self.robber = []
        # creates a new PrettyPrinter for debugging
        p = pprint.PrettyPrinter()

        # Get a deck of the hexes to be placed on the board
        all_hexes = Board.get_shuffled_hex_deck()

        if not starting_board:
            # sets up all_hex_nums
            for i in range(2):
                for x in range(2, 13):
                    # does not add a number token with 7
                    if x != 7:

                        # only adds one 2 and one 12
                        if x == 2 or x == 12:
                            if i == 0:
                                self.all_hex_nums.append(x)

                        # adds two of everything else
                        else:
                            self.all_hex_nums.append(x)

            # shuffles the hex numbers
            random.shuffle(self.all_hex_nums)
            self.hexes = []
            self.hex_nums = []
            last_index = 0

            for r in range(5):
                # the length of this row of hexes
                length = round(-math.fabs(r - 2) + 5)
                self.hexes.append([])
                # Add hexes to this row
                for i in range(length):
                    # Get the hex to be added to the board
                    this_hex = Hex(all_hexes.pop(), None, [])
                    # Add a number token unless it is a desert
                    if this_hex.type == HexType.DESERT:
                        self.robber = [r, i]
                    else:
                        this_hex.token_num = self.all_hex_nums.pop()
                    # Add it to the board
                    self.hexes[r].append(this_hex)
        else:
            # reads the starting_board.json file and copies the board from it
            file = open("pycatan/starting_board.json")
            board_json = file.read()
            board_data = json.loads(board_json)

            # copies the hexes
            for i in range(len(board_data['hexes'])):

                self.hexes.append([])
                self.hex_nums.append([])
                for x in range(len(board_data['hexes'][i])):

                    hex = board_data['hexes'][i][x]
                    to_append = None

                    if hex == "fo":
                        to_append = HexType.FOREST

                    elif hex == "fi":
                        to_append = HexType.FIELDS

                    elif hex == "m":
                        to_append = HexType.MOUNTAINS

                    elif hex == "h":
                        to_append = HexType.HILLS

                    elif hex == "p":
                        to_append = HexType.PASTURE

                    else:
                        to_append = HexType.DESERT

                    self.hexes[i].append(to_append)
                    self.hex_nums[i].append(board_data['hex_nums'][i][x])

        # adds None to points for each point on the hexes
        for i in range(6):

            self.points.append([])
            for x in range(round(12 - math.fabs(2 * i - 5))):

                self.points[i].append(None)

        # adds harbors
        # each harbor is around the edge of the board
        # and are separated by n points, when n is a pattern of 2 3 2 repeating
        # so this gets all the points in segments of top, right, left, bottom
        # and then adds them together

        # adds the top and bottom layer
        top = []
        bottom = []

        # the index of the last row
        last = len(self.points) - 1

        # adds the points
        for i in range(len(self.points[0])):
            top.append([0, i])
            bottom.append([last, len(self.points[0]) - 1 - i])

        # adds all the points on the right and left
        right = []
        left = []

        for r in range(1, len(self.points) - 1):
            length = len(self.points[r]) - 1

            # orders the points depending if they are on the top half or bottom half
            if r < (len(self.points) - 1) / 2:
                right.append([r, length - 1])
                right.append([r, length])

                left.append([len(self.points) - 1 - r, 1])
                left.append([len(self.points) - 1 - r, 0])

            else:
                right.append([r, length])
                right.append([r, length - 1])

                left.append([len(self.points) - 1 - r, 0])
                left.append([len(self.points) - 1 - r, 1])

        outside_points = []
        outside_points.extend(top)
        outside_points.extend(right)
        outside_points.extend(bottom)
        outside_points.extend(left)

        # adds a harbor for each points in the pattern 2 3 2 2 3 2 etc

        # the index of the outside point to build a harbor on
        index = 0
        # the count of harbors build
        count = 0
        # the pattern of spaces between harbors
        pattern = [2, 3, 2]
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

        # shuffles the harbors
        random.shuffle(harbor_types)
        # goes around the board once and adds harbors
        while index < len(outside_points):

            # creates a new harbor
            harbor = Harbor(point_one=outside_points[index], point_two=outside_points[index + 1], type=harbor_types[count])
            # adds it to harbors
            self.harbors.append(harbor)
            # increments index by the next pattern, adds one to fit with the width of each harbor being 2
            index += pattern[count % 3] + 1
            # adds one to count
            count += 1

        # puts the robber on the desert hex to start
        for r in range(len(self.hexes)):
            # checks if this row has the desert
            if self.hexes[r].count(HexType.DESERT) > 0:
                # places the robber
                self.robber = [r, self.hexes[r].index(HexType.DESERT)]

   # gives the players cards for a certain roll
    def add_yield(self, roll):

        for r in range(len(self.points)):
            for i in range(len(self.points[r])):
                if self.points[r][i] != None:
                    hex_indexes = self.get_hexes_for_point(r, i)

                    # checks if any hexes have the right number
                    for num in hex_indexes:

                        # makes sure the robber isn't there
                        if self.robber[0] == num[0] and self.robber[1] == num[1]:
                            # skips this hex
                            continue

                        if self.hexes[num[0]][num[1]].token_num == roll:
                            # adds the card to the player's inventory
                            owner = self.points[r][i].owner
                            # gets the card type
                            hex_type = self.hexes[num[0]][num[1]].type
                            card_type = Board.get_card_from_hex(hex_type)
                            # adds two if it is a city
                            if self.points[r][i].type == Building.BUILDING_CITY:
                                (self.game).players[owner].add_cards([
                                    card_type,
                                    card_type
                                ])

                            else:
                                (self.game).players[owner].add_cards([
                                    card_type
                                ])

    # returns the card associated with the hex
    # for example, Brick for Hills, Wood for forests, etc
    @staticmethod
    def get_card_from_hex(hex):

        # returns the appropriete card
        if hex == HexType.FOREST:
            return ResCard.WOOD

        elif hex == HexType.HILLS:
            return ResCard.BRICK

        elif hex == HexType.PASTURE:
            return ResCard.SHEEP

        elif hex == HexType.FIELDS:
            return ResCard.WHEAT

        elif hex == HexType.MOUNTAINS:
            return ResCard.ORE

        else:
            return None

    # returns all the hexes connected to a certain point
    def get_hexes_for_point(self, r, i):
        # the indexes of the hexes
        hex_indexes = []
        # gets the adjacent hexes differently depending on whether the point is in the top or the bottom
        if r < len(self.points) / 2:
            # gets the hexes below the point ------------------

            # adds the hexes to the right
            if i < len(self.points[r]) - 1:
                hex_indexes.append([r, math.floor(i / 2)])

            # if the index is even, the number is between two hexes
            if i % 2 == 0 and i > 0:
                hex_indexes.append([r, math.floor(i / 2) - 1])

            # gets the hexes above the point ------------------

            # gets the hex to the right
            if i > 0 and i < len(self.points[r]) - 2:
                hex_indexes.append([r - 1, math.floor((i - 1) / 2)])

            # gets the hex to the left
            if i % 2 == 1 and i < len(self.points[r]) - 1 and i > 1:
                hex_indexes.append([r - 1, math.floor((i - 1) / 2) - 1])

        else:

            # adds the below -------------

            # gets the hex to the right or directly below
            if i < len(self.points[r]) - 2 and i > 0:
                hex_indexes.append([r, math.floor((i - 1) / 2)])

            # gets the hex to the left
            if i % 2 == 1 and i > 1 and i < len(self.points[r]):
                hex_indexes.append([r, math.floor((i - 1) / 2 - 1)])

            # gets the hexes above ------------

            # gets the hex above and to the right or directly above
            if i < len(self.points[r]) - 1:
                hex_indexes.append([r - 1, math.floor(i / 2)])

            # gets the hex to the left
            if i > 1 and i % 2 == 0:
                hex_indexes.append([r - 1, math.floor((i - 1) / 2)])

        return hex_indexes

    # adds a Building object to the board
    def add_building(self, building, r, i):
        print("ASDF")
        self.points[r][i] = building

    # adds a Building object, which must be a road
    # since roads record their own position and are not in self.points
    def add_road(self, road):
        self.roads.append(road)

    # upgrades an existing settlement to a city
    def upgrade_settlement(self, player, r, i):

        # checks there is a settlement at r, i
        if self.points[r][i] == None:
            return Statuses.ERR_NOT_EXIST

        # checks the settlement is controlled by the correct player
        # if no player is specified, uses the current controlling player
        if self.points[r][i].owner != player:
            return Statuses.ERR_BAD_OWNER

        # checks it is a settlement and not a city
        if self.points[r][i].type != Building.BUILDING_SETTLEMENT:
            return Statuses.ERR_UPGRADE_CITY

        # checks the player has the cards
        needed_cards = [
            ResCard.WHEAT,
            ResCard.WHEAT,
            ResCard.ORE,
            ResCard.ORE,
            ResCard.ORE
        ]
        if not (self.game).players[player].has_cards(needed_cards):
            return Statuses.ERR_CARDS

        # removes the cards
        (self.game).players[player].remove_cards(needed_cards)
        # changes the settlement to a city
        self.points[r][i].type = Building.BUILDING_CITY
        # adds another victory point
        (self.game).players[player].victory_points += 1

        return Statuses.ALL_GOOD

    # gets all the buildings on the board
    def get_buildings(self):

        buildings = []
        for r in range(len(self.points)):
            for i in range(len(self.points[r])):
                if self.points[r][i] != None:
                    buildings.append([r, i])

        return buildings

    # moves the robber to a givne coord
    def move_robber(self, r, i):
        self.robber = [r, i]

    # checks if a point on the board is empty
    def point_is_empty(self, r, i):
        if self.points[r][i] == None:
            return True

        return False

    # checks if a point exists on the board
    def point_exists(self, r, i):
        if r >= 0 and r < len(self.points):
            if i >= 0 and i < len(self.points[r]):
                return True

        return False

    # gets the points that are connected to the point given
    def get_connected_points(self, r, i):

        # the connected points
        connected_points = []
        # whether the point has another point directly above or directly below
        has_point_above = False

        # half of the last index
        # if the board has 6 rows, this will be 2.5
        # so that ceiling/flooring will give the two middle rows
        half_height = (len(self.points) - 1) / 2

        # if it is in the top half
        if r < half_height:

            # even points have a point below, odd points have one above
            if i % 2 == 0:

                # adds a point below

                if r == math.floor(half_height):
                    # this connection has the same index because it is crossing over the middle
                    connected_points.append([r + 1, i])

                else:
                    connected_points.append([r + 1, i + 1])

            else:
                # adds a point above
                if r > 0 and i > 0:
                    connected_points.append([r - 1, i - 1])

        # if it is in the bottom half
        else:
            if i % 2 == 0:

                # adds a point above
                if r == math.ceil(half_height):
                    # same index because it is crossing the middle
                    connected_points.append([r - 1, i])

                else:
                    connected_points.append([r - 1, i + 1])

            else:

                # adds a point below
                if r < len(self.points) - 1 and i > 0:
                    connected_points.append([r + 1, i - 1])

        # # The different in index
        # #
        # #          ABOVE   | BELOW
        # # TOP    |   -1    |   +1
        # # BOTTOM |   +1    |   -1

        # gets the adjacent points
        if i > 0:
            connected_points.append([r, i - 1])

        if i < len(self.points[r]) - 1:
            connected_points.append([r, i + 1])

        return connected_points

    def __repr__(self):
        return ("Board Object")

    # Get a shuffled deck of the correct number of each type of hex in a board
    @staticmethod
    def get_shuffled_hex_deck():
        deck = []
        # sets up all_hexes
        for i in range(4):

            # adds four fields, forests and pastures
            deck.append(HexType.FIELDS)
            deck.append(HexType.FOREST)
            deck.append(HexType.PASTURE)
            # adds three mountains and hills
            if i < 3:
                deck.append(HexType.MOUNTAINS)
                deck.append(HexType.HILLS)

            # adds one desert
            if i == 0:
                deck.append(HexType.DESERT)

        # shuffles the deck
        random.shuffle(deck)
        return deck
