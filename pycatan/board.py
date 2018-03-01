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

import abc

# used for debugging
import pprint

# Base class for different Catan boards
# Should not be instantiated, otherwise the board will be empty
class Board(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self, game):
        # The game the board is in
        self.game = game
        # The hexes on the board
        # Should be set in a subclass
        self.hexes = ()
        # The points on the board
        # Where the players can place settlements/cities
        # Will be set at the end of __init__
        self.points = ()
        # The roads
        self.roads = []
        # The locations of the harbors
        self.harbors = []
        # The location of the robber
        # going r, i
        self.robber = []

    # gives the players cards for a certain roll
    def add_yield(self, roll):

        for r in self.points:
            for p in r:
                # Check there is a building on the point
                if p.building != None:
                    building = p.building
                    hexes = p.hexes

                    # checks if any hexes have the right number
                    for current_hex in hexes:

                        # makes sure the robber isn't there
                        if self.robber[0] == current_hex.position[0] and self.robber[1] == current_hex.position[1]:
                            # skips this hex
                            continue

                        if current_hex.token_num == roll:
                            # adds the card to the player's inventory
                            owner = building.owner
                            # gets the card type
                            card_type = Board.get_card_from_hex(current_hex.type)
                            # adds two if it is a city
                            if building.type == Building.BUILDING_CITY:
                                self.game.players[owner].add_cards([
                                    card_type,
                                    card_type
                                ])

                            else:
                                self.game.players[owner].add_cards([
                                    card_type
                                ])


    # adds a Building object to the board
    def add_building(self, building, r, i):
        self.points[r][i].building = building

    # adds a Building object, which must be a road
    # since roads record their own position and are not in self.points
    def add_road(self, road):
        self.roads.append(road)

    # upgrades an existing settlement to a city
    def upgrade_settlement(self, player, r, i):
        # Get building at point
        building = self.points[r][i].building

        # checks there is a settlement at r, i
        if building == None:
            return Statuses.ERR_NOT_EXIST

        # checks the settlement is controlled by the correct player
        # if no player is specified, uses the current controlling player
        if building.owner != player:
            return Statuses.ERR_BAD_OWNER

        # checks it is a settlement and not a city
        if building.type != Building.BUILDING_SETTLEMENT:
            return Statuses.ERR_UPGRADE_CITY

        # checks the player has the cards
        needed_cards = [
            ResCard.WHEAT,
            ResCard.WHEAT,
            ResCard.ORE,
            ResCard.ORE,
            ResCard.ORE
        ]
        if not self.game.players[player].has_cards(needed_cards):
            return Statuses.ERR_CARDS

        # removes the cards
        self.game.players[player].remove_cards(needed_cards)
        # changes the settlement to a city
        building.type = Building.BUILDING_CITY
        # adds another victory point
        self.game.players[player].victory_points += 1

        return Statuses.ALL_GOOD

    # gets all the buildings on the board
    def get_buildings(self):

        buildings = []
        for r in self.points:
            for p in r:
                if p.building != None:
                    buildings.append(p.building)

        return buildings

    # moves the robber to a givne coord
    def move_robber(self, r, i):
        self.robber = [r, i]

    # checks if a point on the board is empty
    def point_is_empty(self, r, i):
        if self.points[r][i].building == None:
            return True

        return False

    # checks if a point exists on the board
    def point_exists(self, r, i):
        if r >= 0 and r < len(self.points):
            if i >= 0 and i < len(self.points[r]):
                return True

        return False

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

    @staticmethod
    def get_shuffled_hex_nums():
        nums = []
        # Get 2 of each number, most of the time
        for i in range(2):
            # Go through each type
            for x in range(2, 13):
                # Does not add a number token with 7
                if x != 7:
                    # Only adds one 2 and one 12
                    if x == 2 or x == 12:
                        if i == 0:
                            nums.append(x)
                    # Adds two of everything else
                    else:
                        nums.append(x)
        random.shuffle(nums)
        return nums

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
